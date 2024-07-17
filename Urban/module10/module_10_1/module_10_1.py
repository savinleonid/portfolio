from time import sleep
from datetime import datetime
from threading import Thread


def wite_words(word_count, file_name):
    with open(file_name, "w", encoding="utf-8") as f:
        for num in range(word_count):
            f.write(f"Some word № {num + 1}\n")
            sleep(0.1)
    print("Finished writing to file", file_name)


# main thread test
start_time = datetime.now()
wite_words(10, "example1.txt")
wite_words(30, "example2.txt")
wite_words(200, "example3.txt")
wite_words(100, "example4.txt")
end_time = datetime.now()
print("Time passed:", end_time - start_time)

# 4 thread test
start_time = datetime.now()
thr_1 = Thread(target=wite_words, args=(10, "example5.txt"))
thr_2 = Thread(target=wite_words, args=(30, "example6.txt"))
thr_3 = Thread(target=wite_words, args=(200, "example7.txt"))
thr_4 = Thread(target=wite_words, args=(100, "example8.txt"))

thr_1.start()
thr_2.start()
thr_3.start()
thr_4.start()

thr_1.join()
thr_2.join()
thr_3.join()
thr_4.join()

end_time = datetime.now()
print("Time passed:", end_time - start_time)
