#csv---标准库模块
import csv

with open('风云.csv','a',newline='') as f:
    writer=csv.writer(f)
    writer.writerow(['聂风','刀'])
    writer.writerow(['步惊云','剑'])
    writer.writerow(['熊吧','气'])
