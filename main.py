import sys
import json
import argparse
import configparser

#instancemap = json.loads(open('instance_type.json').read())
def getnearsize(instancemap,cpus,rams):
    filterd_sizes = []
    for x,y in instancemap.items():
        if y['cpu'] >= cpus:
            if y['ram'] >= rams:
                filterd_sizes.append((x,y['cpu']*y['ram']))
    sorted_filterd_sizes = sorted(filterd_sizes,key=lambda x:x[1])
    if len(sorted_filterd_sizes) == 0 :
        return None
    else:
        final_choice = sorted_filterd_sizes[0][0]
        return final_choice

def getsizing(instancemap,prefferedsizing,cpus,rams):
    outputmap = {}
    icpu=instancemap[prefferedsizing]['cpu']
    iram=instancemap[prefferedsizing]['ram']
    if cpus < icpu or rams < iram:
        outputmap[prefferedsizing]=1
        return outputmap
    else:
        ccount,rcpus=divmod(cpus,icpu)
        rcount,rrams=divmod(rams,iram)
        if ccount == rcount:
            outputmap[prefferedsizing]=ccount
            print('Remaining CPU: {}  & RAM: {}'.format(rcpus,rrams))
        else:
            count=min(ccount,rcount)
            outputmap[prefferedsizing]=count
            rcpus=cpus - (count * icpu)
            rrams=rams - (count * iram)
            print('Remaining CPU: {}  & RAM: {}'.format(rcpus,rrams))
            filterd_sizes = []
            for x,y in instancemap.items():
                if y['cpu'] >= rcpus:
                    if y['ram'] >= rrams:
                        filterd_sizes.append((x,y['cpu']*y['ram']))
            sorted_filterd_sizes = sorted(filterd_sizes,key=lambda x:x[1])
            final_choice= sorted_filterd_sizes[0][0]
            rcpus=rcpus-instancemap[final_choice]['cpu']
            rrams=rrams-instancemap[final_choice]['ram']
            print('Remaining CPU: {}  & RAM: {}'.format(rcpus,rrams))
            outputmap[final_choice]=1
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
