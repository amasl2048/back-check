# Backup and check

Copy files to different destinations and check md5 sums.

List source files to backup:
```
$ cat ./backup.list
./src1/file1
./src2/file2
```

Destination directories to copy:
```
$ cat ./backup_cfg.yml
---
dest_dirs:
    - "./dest1"
    - "./dest2"
```

Run python script to backup files and check md5 sums:
```
$ python3 ./back_check.py 

Starting... 
---
Check remote and copy files...
./dest2
copied ./dest2/file1 

./dest1
copied ./dest1/file2 

Check md5sums...
./dest2
| file1 | 83fabf57b06b6837d70a644fe6a4d708 | == | 83fabf57b06b6837d70a644fe6a4d708 |
| file2 | 1180d91eb7c7820f51e03a5b0e61bceb | == | 1180d91eb7c7820f51e03a5b0e61bceb |
./dest1
| file1 | 83fabf57b06b6837d70a644fe6a4d708 | == | 83fabf57b06b6837d70a644fe6a4d708 |
| file2 | 1180d91eb7c7820f51e03a5b0e61bceb | == | 1180d91eb7c7820f51e03a5b0e61bceb |
Done.
```

Change files `./src1/file1`, `./dest2/file2` and then run the scipt again:
```
$ python3 ./back_check.py 

Starting... 
---

Check remote and copy files...
./dest1
./dest2

Check md5sums...
./dest1
| file1 | 6b99df4a28879323097ce2a752a2bab4 | -> | 83fabf57b06b6837d70a644fe6a4d708 |
copied file1 
| file2 | 1180d91eb7c7820f51e03a5b0e61bceb | == | 1180d91eb7c7820f51e03a5b0e61bceb |

./dest2
| file1 | 6b99df4a28879323097ce2a752a2bab4 | -> | 83fabf57b06b6837d70a644fe6a4d708 |
copied file1 
| file2 | 14.06.2021 19:29:00 | ->  | 17.06.2021 20:50:17 |
| file2 | 1180d91eb7c7820f51e03a5b0e61bceb | -> | c038623ced6c4155a483ec90e4ab9f90 |
copied file2 

Done.
```

`file1` is updated on both destinations, `file2` updated on dest2:
```
$ ls ./dest*
./dest1:
file1  file1.1.bak  file2

./dest2:
file1  file1.1.bak  file2  file2.1.bak
```
