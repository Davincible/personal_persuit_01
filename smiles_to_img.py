#!/bin/python3

from multiprocessing import Process, Queue
import requests
import os
import time
import urllib

source_path = "data/drugs.smi"

output_folder = "data/smiles_images"

if not os.path.exists(output_folder):
    os.mkdir(output_folder)


print("Reading in smiles data")
stack = Queue()
batch_size = 25000
with open(source_path, 'r') as file:
    for line in range(batch_size):
        smiles = file.readline().strip()
        stack.put(smiles)
        if line % (batch_size // 3) == 0:
            print("At itteration:", line)
print()
        
def to_img(q, out_path, prefix, start_time):
    itter = 1
    while not q.empty():
        smiles = q.get()
        smiles = urllib.parse.quote(smiles, safe='')
        base_url = f"http://hulab.rxnfinder.org/smi2img/{smiles}/?width=300&height=300"
        response = requests.get(base_url, stream=True)
        if response.status_code == 200 and "error" not in response.text.lower():
            path = out_path + '/' + prefix + str(itter) + ".png"
            with open(path, 'wb') as file:
                for chunk in response:
                    file.write(chunk)
            itter += 1
        else:
            print("bad url", response.status_code, smiles)
        print(int(time.time() - start_time), ':', q.qsize())

start = time.time()
p1 = Process(target=to_img, args=(stack, output_folder, "one", start))
p2 = Process(target=to_img, args=(stack, output_folder, "two", start))
p3 = Process(target=to_img, args=(stack, output_folder, "three", start))
p4 = Process(target=to_img, args=(stack, output_folder, "four", start))
p5 = Process(target=to_img, args=(stack, output_folder, "five", start))

p1.start()
p2.start()
p3.start()
p4.start()
p5.start()

p1.join()
p2.join()
p3.join()
p4.join()
p5.join()


