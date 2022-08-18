import argparse
import torch.optim as optim
import torch.nn.modules as nn
import models
from utils import *
from dataloader import make_dataloader

def main():
    '''
    argparse는 터미널 창에서 입력을 파싱할 수 있게 도와줌
    예를 들어 main 함수에서 설정하는 변수인 model을 직접 코드를 수정하지 않고 터미널에서 코드 실행시에
    python main.py --model XXX 형태로 실행하면 model을 XXX로 결정할 수 있음

    변수 종류
    model: 뉴럴 네트워크 구조를 의미
        group1 - resnet8, resnet14, resnet20, resnet32, resnet44, resnet56, resnet110, resnet8x4, resnet32x4
        group2 - resnet18, resnet34, resnet50, resnet101, resnet152
        group2의 parameter가 일반적으로 많고 성능이 좋지만 학습에 시간이 오래걸림, 숫자는 layer 수를 의미하며 layer
        수가 많아질수록 일반적으로 성능이 좋아짐
    data_dir: digit_data 폴더가 있는 경로
    size: 입력 이미지의 크기, 크기가 클수록 성능이 좋아질 수 있지만, 연산량이 커지기 때문에 적절한 크기 세팅 필요
          (default: 64)
    batch_size: 한 번의 iteration에 사용되는 data instance의 수
    epochs: dataset 전체를 몇 번 사용하여 학습할 지 결정하는 요소로 1 epoch에 전체 dataset의 모든 instance를 1회 사용
    optimizer: 뉴럴 네트워크의 parameter를 학습시키는 방법을 결정 (sgd, adam)
    lr: 학습을 처음 시작할 때 결정하는 learning rate의 값. 한 번의 iteration에서 parameter를 얼마나 update 시킬지
        결정하는 값 클수록 한 번에 크게 parameter를 update 하지만, learning rate가 너무 큰 경우 학습이 잘 안될 수 있음
    scheduler: learning rate를 조절하는 스케쥴을 결정 (cosine, poly, exponential)
    weight_decay: 모델이 training data에 과적합되는 것을 막기 위해 정규화시키는 정도를 결정

    터미널 창 사용 예시
    python main.py --model resnet8 --data_dir ../../digit_data --size 64 --batch_size 128 --epochs 100 \
    --optimizer adam --lr 0.001 --scheduler cosine --weight_decay 5e-4
    위와 같이 띄어쓰기로 argument 구분
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='resnet8', help='network architecture, resnet is only implemented')
    parser.add_argument('--data_dir', default='../../digit_data', type=str, help='digit data directory')
    parser.add_argument('--size', default=64, type=int, help='size of resized image')
    parser.add_argument('--batch_size', default=128, type=int, help='batch size')

    parser.add_argument('--epochs', default=100, type=int, help='number of training epochs')
    parser.add_argument('--optimizer', default='adam', type=str, help='optimizer')
    parser.add_argument('--lr', default=0.001, type=float, help='learning rate')
    parser.add_argument('--scheduler', default='cosine', type=str, help='learning rate scheduler, cosine, poly ...')
    parser.add_argument('--weight_decay', default=5e-4, type=float, help='weight decay for l2 regularization')

    args = parser.parse_args() # argument를 parsing

    checkname = '_'.join([args.model, str(args.size), str(args.batch_size), str(args.epochs), args.optimizer, str(args.lr),
                          args.scheduler, str(args.weight_decay)]) # 저장하는 log 파일 및 weight 파일의 이름

    args.cuda = torch.cuda.is_available() # GPU 사용 가능 여부 확인
    model = models.__dict__[args.model](num_classes=10) # 모델 선택
    if args.cuda:
        model.cuda() # GPU 사용이 가능한 경우, GPU 사용
    train_loader, valid_loader = make_dataloader(args.data_dir, args.size, args.batch_size) # data loader 불러오기 (dataloader.py 참고)

    # optimizer 선정
    if args.optimizer == 'sgd':
        optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=0.9, weight_decay=args.weight_decay)
    else:
        optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    # scheduler 선정
    if args.scheduler == 'cosine':
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, args.epochs)
    elif args.scheduler == 'poly':
        scheduler = optim.lr_scheduler.LambdaLR(optimizer, lambda x: (args.lr * (1.0 - x / args.epochs) ** 0.9))
    elif args.scheduler == 'exponential':
        scheduler = optim.lr_scheduler.ExponentialLR(optimizer, 0.99)
    else:
        raise NotImplementedError

    criterion = nn.CrossEntropyLoss() # loss function 선정
    saver = Saver(args, checkname) # log 및 학습된 모델의 저장을 위해 saver 생성 (utils.py의 Saver class 참고)
    # training, validation 시작 및 로그 기록 (utils.py의 train, valid 함수 참고)
    for epoch in range(args.epochs):
        train_loss, train_acc = train(model, train_loader, criterion, optimizer, args.cuda)
        valid_acc = valid(model, valid_loader, saver, args.cuda)
        scheduler.step()
        saver.logger.info('Epoch: {0:>3d}| Train loss: {1:0.4f}| Train Acc: {2:0.4f}| Valid Acc: {3:0.4f}'
                          .format(epoch + 1, train_loss, train_acc, valid_acc))


if __name__ == '__main__':
    main() # main 함수 실