import sqlite3
import json
import argparse

def query_db(db_name):
    conn = sqlite3.connect(db_name, check_same_thread=False)
    c = conn.cursor()

    c.execute(f"SELECT * FROM {TABLE_NAME}")

    row = c.fetchall()

    conn.close()

    row.sort(key=lambda x:x[IDX_TS])

    return row


def load_id2seq_map(path):
    with open(path) as json_file:
        idmap = json.load(json_file)

    return idmap

def append_trace(outputbuffer, outputarray):
    trace = []
    for i in range(len(outputbuffer)):
        trace.append(outputbuffer[i])

    outputarray.append(trace)


def filter_trace(data):
    ret_data = []
    for row in data:
        if row[IDX_DURATION] > epsilon:
            ret_data.append(row)

    return ret_data

def get_average_trace(data):
    total_duration = {}
    video_count = {}
    video_duration = {}
    video_length = {}
    for i in range(len(data)):
        vid = data[i][IDX_VID]
        if vid not in total_duration.keys():
            total_duration[vid] = data[i][IDX_DURATION]
            video_count[vid] = 1
            video_length[vid] = data[i][IDX_LEN]

        else:
            total_duration[vid] += data[i][IDX_DURATION]
            video_count[vid] += 1

    for vid in total_duration.keys():
        video_duration[vid] = total_duration[vid] / video_count[vid]

    return video_duration, video_length

def fix_individual_trace(trace, id_list, id_map, video_duration, video_length):
    """
    The goal is to fix the missing entry and also duplication
    :param trace: The trace to process
    :param id_list: The list from sequence number to video id
    :param id_map: The map from video id to sequence number
    :param video_duration: The map from video id to video duration
    :param video_length: The map from video id to video length
    :return: fixed trace
    """
    trace_fixed = []

    seq = 0
    idx = 0

    last_seq = id_map[trace[-1][IDX_VID]]

    if id_map[trace[0][IDX_VID]] != 0:
        vid = id_list[seq]
        trace_fixed.append([
            trace[0][IDX_IP],
            vid,
            video_length[vid],
            video_duration[vid],
            0,
            trace[0][IDX_TS_STR],
            seq,
            ])
        seq += 1

    while seq <= last_seq:
        if seq == id_map[trace[idx][IDX_VID]]:
            trace_fixed.append([
                trace[idx][IDX_IP],
                trace[idx][IDX_VID],
                trace[idx][IDX_LEN],
                trace[idx][IDX_DURATION],
                trace[idx][IDX_TS],
                trace[idx][IDX_TS_STR],
                id_map[trace[idx][IDX_VID]],
                ])
            idx += 1
            seq += 1

        # duplication
        elif seq > id_map[trace[idx][IDX_VID]]:
            trace_fixed[id_map[trace[idx][IDX_VID]]] = [
                trace[idx][IDX_IP],
                trace[idx][IDX_VID],
                trace[idx][IDX_LEN],
                trace[idx][IDX_DURATION],
                trace[idx][IDX_TS],
                trace[idx][IDX_TS_STR],
                id_map[trace[idx][IDX_VID]],
            ]
            idx += 1

        # missing
        else:
            vid = id_list[seq]
            last_entry = trace_fixed[-1]
            trace_fixed.append([
                last_entry[IDX_IP],
                vid,
                video_length[vid],
                video_duration[vid],
                last_entry[IDX_TS] + epsilon,
                last_entry[IDX_TS_STR],
                seq,
            ])
            seq += 1

    return trace_fixed


def dump_trace(trace, fname):
    fd = open(fname, "w")

    for entry in trace:
        fd.write(f"{entry[IDX_LEN]} {entry[IDX_DURATION]} {entry[IDX_SEQ]}\n")
    fd.close()


def main(args):
    data_raw = query_db(args.db)

    data_filtered = filter_trace(data_raw)
    id_map = load_id2seq_map(args.id2seq)

    video_duration, video_length = get_average_trace(data_filtered)

    id_list = ["" for i in range(len(id_map))]
    length_list = [0.0 for i in range(len(id_map))]

    for key in id_map.keys():
        id_list[id_map[key]] = key

    # put the each user's corresponding trace into the user to trace map
    user2trace_map = {}

    for i in range(len(data_filtered)):
        if data_filtered[i][IDX_IP] not in user2trace_map.keys():
            user2trace_map[data_filtered[i][IDX_IP]] = []

        user2trace_map[data_filtered[i][IDX_IP]].append(list(data_filtered[i]))

        length_list[id_map[data_filtered[i][IDX_VID]]] = data_filtered[i][IDX_LEN]

    # start to process each user's trace
    for ip in user2trace_map.keys():
        print(ip)

        outputbuffer = []

        # outputarray is a two-dimensional array, each row is a user trace.
        outputarray = []

        view_trace = user2trace_map[ip]
        for item in view_trace:
            # id map to zero means the start of a new trace
            if id_map[item[IDX_VID]] != 0:
                outputbuffer.append(item)
            else:
                if len(outputbuffer) >= SKIP_THRESHOLD:
                    append_trace(outputbuffer, outputarray)

                outputbuffer = []
                outputbuffer.append(item)

        # append the remaining item from the outputbuffer to outputarray
        if len(outputbuffer) >= SKIP_THRESHOLD:
            append_trace(outputbuffer, outputarray)

        if len(outputarray) == 0:
            continue

        for trace_id in range(len(outputarray)):
            if id_map[outputarray[trace_id][0][IDX_VID]] > 3:
                print("skip")
                continue

            if abs(id_map[outputarray[trace_id][-1][IDX_VID]] - len(outputarray[trace_id])) > 20:
                continue

            max_length = min(len(outputarray[trace_id]), 300)
            trace_in = outputarray[trace_id][0:max_length]
            trace_fixed = fix_individual_trace(trace_in, id_list, id_map, video_duration, video_length)

            fname = f"{args.savepath}/{ip}-{trace_id}.txt"
            dump_trace(trace_fixed, fname)


if __name__=="__main__":

    IDX_IP = 0
    IDX_VID = 1
    IDX_LEN = 2
    IDX_DURATION = 3
    IDX_TS = 4
    IDX_TS_STR = 5
    IDX_SEQ = 6

    epsilon = 0.00001

    SKIP_THRESHOLD = 30

    TABLE_NAME = "DATASET"

    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default='data-all.db', help='The database to query')
    parser.add_argument('--id2seq', default='vid.json', help='The id to sequence number mapping')
    parser.add_argument('--savepath', default='./data', help='The path to save processed data')

    args = parser.parse_args()
    main(args)
