# EMBER2024

EMBER2024 is an update to the [EMBER2017 and EMBER2018](https://github.com/elastic/ember/) datasets. It includes raw features and labels for 3.2 million malicious and benign files from 6 different file types (Win32, Win64, .NET, APK, ELF, and PDF). EMBER2024 is meant to allow researchers to explore a variety of common malware analysis classification tasks. The dataset includes 7 types of labels and tags that support malicious/benign detection, malware family classification, malware behavior prediction, and more.

For more details, check out our [paper](https://arxiv.org/pdf/2506.05074)!


## EMBER2024 Contents

EMBER2024 includes features and labels for malware that was first uploaded to VirusTotal between Sep. 24th, 2023 and Dec. 14th, 2024. There are exactly 50,500 files chosen from each week of that time period, with the first 52 weeks of files making up the training set and the last 12 going to the test set. This lets researchers simulate how effectively a classifier might detect malware that is newer than its training corpus. In total, the training set is 2,626,000 files and the test set is 606,000 files.

#### File Statistics
| File Type   | Malicious + Benign (Weekly) | Train Total | Test Total |
| -------- | ------- | ------ | ------- |
| Win32  | 30,000    | 1,560,000 | 360,000 |
| Win64 | 10,000     | 520,000 | 120,000 |
| .NET    | 5,000    | 260,000 | 60,000 |
| APK  | 4,000    | 208,000 | 48,000 |
| PDF | 1,000  | 52,000 | 12,000 |
| ELF    | 500    | 26,000 | 6,000 |

#### Challenge Set

EMBER also includes features and labels for 6,315 malicious files in a "challenge set". These files initially went undetected by ~70 antivirus products on VirusTotal but were later found to be malicious. The challenge set is an excellent resource for assessing how well a machine larning classifier is able to detect evasive malware.


## EMBER Feature Version 3

The previous EMBER feature versions were pinned to [LIEF](lief.re) version 0.9.0, which requires Python 3.6. EMBER feature version 3 ("thrember") is a re-implementation of the EMBER feature vector format that uses the [pefile](https://github.com/erocarrera/pefile) library instead. pefile is stable and has no dependencies, making it ideal going forward. We have also made several addition to the EMBER feature vector format, which now includes features from the DOS header, Rich header, PE data directories, Authenticode signatures, and warnings during PE parsing. Furthermore, we have added support for feature extraction from non-PE files using a subset of the EMBER feature version 3 format. We show that effective classifiers for APK, ELF, and PDF files can be trained using just features from general file info, byte statistics, and string statistics.

## Installation

To clone the repository and install it using pip, run:
```
git clone https://github.com/FutureComputing4AI/EMBER2024.git
cd EMBER2024/
pip install .
```


## Download Models and Dataset

The EMBER2024 models, features, and labels are hosted on HuggingFace. To download them from the HuggingFace hub, launch a Python console, import thrember, and run the download_models() and/or download_dataset() functions:

#### Downloading the models

To download the 14 benchmark LightGBM classifiers we trained on EMBER2024, run:

```
thrember.download_models("/path/to/download/to/")
```


#### Downloading the data:

```
import thrember
thrember.download_dataset("/path/to/download/to/")
```

You can download smaller chunks of the dataset by passing different keyword arguments to download_dataset.py:

Download all PE (Win32, Win64, and .NET) files:
```
thrember.download_dataset("/path/to/download/to/" file_type="PE")
```

Download just the APKs in the training set:
```
thrember.download_dataset("/path/to/download/to/" file_type="APK", split="train")
```

Download just the challenge set:

```
thrember.download_dataset("/path/to/download/to/" split="challenge")
```



The sizes of the features and labels for each portion of EMBER2024 are shown below:

| Subset | Total Size |
| ------ | ------ |
| Win32 train | 23.7 GB |
| Win32 test  | 4.9 GB |
| Win64 train | 12.9 GB |
| Win64 test  | 2.5 GB |
| .NET train | 1.8 GB |
| .NET test | 425 MB |
| APK train | 1.0 GB|
| APK test | 234 MB|
| PDF train | 197 MB |
| PDF test | 46 MB |
| ELF train | 100 MB |
| ELF test | 24 MB |
| challenge | 126 MB |


## Vectorizing Raw Features

Depending on which files you choose to download, you can vectorize the entire EMBER2024 dataset or just a part of it. The Python code below will create .dat files with feature vectors and malicious/benign labels for the train, test, and challenge sets.

```
import thrember
thrember.create_vectorized_features('/path/to/dataset/')
```

Families and tags were assigned to files using [ClarAVy](https://github.com/FutureComputing4AI/ClarAVy/). If you want to train a classifier on other types of labels or tags, pass the label_type keyword to the create_vectorized_features() function:

```
thrember.create_vectorized_features('/path/to/dataset/', label_type="family")
thrember.create_vectorized_features('/path/to/dataset/', label_type="behavior")
thrember.create_vectorized_features('/path/to/dataset/', label_type="file_property")
thrember.create_vectorized_features('/path/to/dataset/', label_type="packer")
thrember.create_vectorized_features('/path/to/dataset/', label_type="exploit")
thrember.create_vectorized_features('/path/to/dataset/', label_type="group")
```

By default, any families, behaviors, etc. that occur fewer than 10 times in EMBER2024 are ignored during vectorization. To adjust this, use the class_min keyword:

```
thrember.create_vectorized_features('/path/to/dataset/', label_type="family", class_min=1)
```

## Reading EMBER Vectors

Once you've vectorized EMBER2024, you can read the data and labels into numpy ndarrays:

```
import thrember
X_train, y_train = thrember.read_vectorized_features('/path/to/dataset/', subset="train")
X_test, y_test = thrember.read_vectorized_features('/path/to/dataset/', subset="test")
X_challenge, y_challenge = thrember.read_vectorized_features('/path/to/dataset/', subset="challenge")
```

## More Examples

Check out the ```examples/``` directory for more example code!

```
ember2024-notebook.ipynb -- Explore the EMBER2024 dataset
train_lgbm.py -- Train a LightGBM classifier
eval_lgbm.py -- Evaluate a classifier on the test and challenge sets
```


## Dataset Methodology

To learn more about how we built EMBER2024, check out our [vtpipeline-rs](https://github.com/FutureComputing4AI/vtpipeline-rs) repository!

## Updates!

#### Capa

[Capa](https://github.com/mandiant/capa) is a malware analysis tool that identifies a file's potential behaviors. For each file, it outputs Mitre ATT&CK techniques, objectives and behaviors from the Malware Behavior Catalogue Matrix, and other capabilities. An example is shown below. 

```
+----------------------+---------------------------------------------------------------------------+
| ATT&CK Tactic        | ATT&CK Technique                                                          |
+----------------------+---------------------------------------------------------------------------+
| COLLECTION           | Clipboard Data [T1115]                                                    |
|                      | Input Capture::Keylogging [T1056.001]                                     |
|                      | Screen Capture [T1113]                                                    |
| DEFENSE EVASION      | File and Directory Permissions Modification [T1222]                       |
|                      | Obfuscated Files or Information [T1027]                                   |
| EXECUTION            | Shared Modules [T1129]                                                    |
| PRIVILEGE ESCALATION | Access Token Manipulation [T1134]                                         |
| ...                  | ...                                                                       |
+----------------------+---------------------------------------------------------------------------+

+----------------------+---------------------------------------------------------------------------+
| MBC Objective            | MBC Behavior                                                          |
+----------------------+---------------------------------------------------------------------------+
| ANTI-BEHAVIORAL ANALYSIS | Debugger Detection::Software Breakpoints [B0001.025]                  |
|                          | Debugger Detection::Timing/Delay Check GetTickCount [B0001.032]       |
| COLLECTION               | Keylogging::Polling [F0002.002]                                       |
|                          | Screen Capture::WinAPI [E1113.m01]                                    |
| COMMAND AND CONTROL      | C2 Communication::Receive Data [B0030.002]                            |
|                          | C2 Communication::Send Data [B0030.001]                               |
| ...                      | ...                                                                   |
+----------------------+---------------------------------------------------------------------------+

+----------------------+---------------------------------------------------------------------------+
| Capability                                          | Namespace                                  |
+----------------------+---------------------------------------------------------------------------+
| log keystrokes via polling (9 matches)              | collection/keylog                          |
| capture screenshot (2 matches)                      | collection/screenshot                      |
| receive data (5 matches)                            | communication                              |
| send data (2 matches)                               | communication                              |
| create HTTP request                                 | communication/http/client                  |
| get socket status                                   | communication/socket                       |
| ...                                                 | ...                                        |
+----------------------+---------------------------------------------------------------------------+
```

EMBER2024 has been updated to include Capa results for Win32, Win64, .NET, and ELF files.

```
{
  "caps": [
    {"Capability": "Find process by name", "Namespace": "host-interaction/process/list", "Addrs": []},
    {"Capability": "Terminate process", "Namespace": "host-interaction/process/terminate", "Addrs": ["0x6000025"]},
    {"Capability": "Move file", "Namespace": "host-interaction/file-system/move", "Addrs": []},
    ...
  ],
  "ttps": [
    {"Tactic": "DISCOVERY", "Technique": "Process Discovery [T1057]"},
    {"Tactic": "DISCOVERY", "Technique": "File and Directory Discovery [T1083]"}
  ],
  "mbc": [
    {"Objective": "OPERATING SYSTEM", "Behavior": "Console [C0033]"},
    {"Objective": "PROCESS", "Behavior": "Terminate Process [C0018]"},
    {"Objective": "FILE SYSTEM", "Behavior": "Move File [C0063]"},
    {"Objective": "DISCOVERY", "Behavior": "File and Directory Discovery [E1083]"},
    ....
  ],
  ...
}
```

In many cases, Capa identifies the function(s) that the capability is present in. We created a [supplemental dataset](https://huggingface.co/datasets/joyce8/EMBER2024-capa) with the raw bytes and disassembly of 16,356,790 functions from malicious files in EMBER2024.

## Citing

If you use EMBER2024 in your own research, please cite it using:

```
@inproceedings{joyce2025ember,
      title={EMBER2024 - A Benchmark Dataset for Holistic Evaluation of Malware Classifiers},
      author={Robert J. Joyce and Gideon Miller and Phil Roth and Richard Zak and Elliott Zaresky-Williams and Hyrum Anderson and Edward Raff and James Holt},
      year={2025},
      booktitle={Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining},
}
