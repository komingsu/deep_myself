import os
from PIL import Image
from torchvision import transforms
from torch.utils.data.dataloader import DataLoader


class DigitData:
    '''
    digit_data를 pytorch에서 사용 가능한 형태로 변경
    '''
    def __init__(self, path, size=64, split='train'):
        '''
        path: digit_data의 경로
        size: image input의 크기 (default: 64 -> 64 x 64 image를 입력으로 사용)
        split: train, validation 구분
        '''
        self.path = path
        self.size = (size, size)

        # 각 instance 별 경로 읽음
        if split == 'train':
            self.image_files = open(os.path.join(path, 'train_data.txt'), 'r').read().splitlines()
        else:
            self.image_files = open(os.path.join(path, 'valid_data.txt'), 'r').read().splitlines()

        # image dataset 전체의 평균 및 표준편차를 계산하여 normalization 하여 사용
        mean = [0.80048384, 0.44734452, 0.50106468]
        std = [0.22327253, 0.29523788, 0.24583565]
        # 이미지를 뉴럴 네트워크의 input으로 사용하기 위하여 transformation
        self.transform = transforms.Compose([transforms.Resize(self.size), transforms.ToTensor(),
                                             transforms.Normalize(mean=mean, std=std)])

    def __len__(self):
        # len 함수로 표시되는 output
        # 총 data instance의 수
        return len(self.image_files)

    def __getitem__(self, idx):
        # indexing을 하였을 때 나오는 output (예시 Data[5] 등의 output)
        path = os.path.join(self.path, self.image_files[idx])
        img = Image.open(path).convert('RGB') # image 읽기
        img = self.transform(img) # image를 뉴럴 네트워크의 input으로 사용하기 위하여 transformation
        target = int(self.image_files[idx].split('/')[0]) # category (0~9)
        return img, target


def make_dataloader(path, size, batch_size):
    '''
    DigitData를 사용하여 뉴럴네트워크를 학습할 때 데이터의 순서나 한 번의 iteration에 사용되는 batch를 생성
    path: digit_data의 경로
    size: image input의 크기
    batch_size: 한 번의 iteration에 사용될 데이터의 수
    '''
    # Dataset 생성
    train_data = DigitData(path, size, 'train')
    valid_data = DigitData(path, size, 'valid')
    # Batch 별로 input을 나누어 사용할 수 잇도록 data loader 생성
    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
    valid_loader = DataLoader(valid_data, batch_size=batch_size, shuffle=True)
    return train_loader, valid_loader


if __name__ == '__main__':
    data = DigitData('/data/CWT_Weights/digit_data', 64, 'train')
    loader = DataLoader(data, 2, True)
    for (img, target) in loader:
        print(img)
        print(target)
        break