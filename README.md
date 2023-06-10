# kemuri-kenchi 煙検知
Detect when smoke is released.

> ## kemuri-kenchi v1 feedback
> kemuri-kenchi is heading towards v2 and we would love to hear what _**you**_ would like to see in it. 
>
> **Thank you!**

![kemuri-kenchi](asset/logo.jpg?raw=true)

[![Python Version](https://img.shields.io/badge/python%20version-%3E=3.7.6-61CFDD.svg?style=flat-square)](https://www.python.org/downloads/release/python-376/)


## Install

```shell
git clone git@github.com:nanotube164/kemuri-kenchi.git
```

## What is kemuri-kenchi?

kemuri-kenchi is a solution for monitoring smoke released from factory. Belows is the demo.

![](https://github.com/nanotube164/kemuri-kenchi/blob/main/result.gif)


It is designed to track smoking by [Gaussian Mixture Model(GMM)](https://ir.nctu.edu.tw/bitstream/11536/68068/7/251107.pdf).
It supports:

* automately alarm when detect smoking
* distinguish smoke moving from cloud moving.


kemuri-kenchi can be thought of as signal alarm.


## How to activate?

After you unzip the folder, input below in the command line and enter.
```bash=
python main.py
```

## Q & A

### Why is it called “kemuri-kenchi”?

A: Smoke detection in japanese is `kemuri-kenchi` `煙検知`. That's why I name it `kemuri-kenchi`. Just the pronunciation of japanese.

## Connect

Send email to `nicholas.cheng.1106@gmail.com`
