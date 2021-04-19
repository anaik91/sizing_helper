import sys
import json
import argparse
import configparser

def getsizing(instancemap,prefferedsizing,cpus,rams):
    outputmap = {}
    icpu=instancemap[prefferedsizing]['cpu']
    iram=instancemap[prefferedsizing]['ram']
    if cpus < icpu or rams < iram:
        outputmap[prefferedsizing]=1
        return outputmap
    else:
        evalset = {}
        for x,y in instancemap.items():
            evalset[x] = []
            for i in range(1,6):
                evalset[x].append({'count':i, 'cpu': i*y['cpu'] , 'ram': i*y['ram'] })
        filtered = {}
        for eachsize,info in evalset.items():
            filtered[eachsize]=[]
            for eachcombo in info:
                #print(eachcombo)
                if eachcombo['cpu'] >= cpus and eachcombo['ram'] >= rams:
                    wastage = (cpus - eachcombo['cpu']) + (rams - eachcombo['ram'])
                    filtered[eachsize].append({'count':eachcombo['count'],'wastage':wastage ,'cpu': eachcombo['cpu'],'ram': eachcombo['ram']})
        filtered = { a:b for a,b in filtered.items() if len(b) > 0 }
        minwastage=None
        for x,y in filtered.items():
            for each in y:
                if minwastage is None:
                    minwastage = abs(each['wastage'])
                    outputmap[x]={
                            'count': each['count'], 
                            'overprovision': {
                                'cpu': each['cpu'] - cpus,
                                'ram':each['ram'] - rams
                            }
                        }
                else:
                    if  abs(each['wastage']) < minwastage:
                        minwastage = abs(each['wastage'])
                        outputmap[x]={
                            'count': each['count'], 
                            'overprovision': {
                                'cpu': each['cpu'] - cpus,
                                'ram':each['ram'] - rams
                            }
                        }
        return outputmap
            

def main():
    config = configparser.ConfigParser()
    config.read('instance_type.properties')
    instancemap = { i:{'cpu':int(config[i]['cpu']),'ram': int(config[i]['ram'])} 
    for i in config.sections()}
    parser = argparse.ArgumentParser(description='Get AWS EC2 Instance Sizing.')
    parser.add_argument('--default',type=str,
                        default='m5.xlarge',
                        help='Default sizing. Defaults to m5.xlarge')
    parser.add_argument('--cpu',type=int,
                        help='Number of CPUs')
    parser.add_argument('--ram',type=int,
                        help='Number of RAMs')
    args = parser.parse_args()

    sizing = getsizing(instancemap,args.default,args.cpu,args.ram)
    print('Below is Sizing recommendation\n{}'.format(sizing))

if __name__ == '__main__':
    main()
