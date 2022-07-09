import torch
import torchaudio
import torch.nn.functional as F
import numpy as np
from torchaudio.models import ConvTasNet as ctn
from build_dataset import train_data as full_dataset
from torch.utils.data import random_split, Dataset, DataLoader

model = ctn(2,2,32)

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

model = model.to(device)


optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


def train(model, optimizer, loss_fn, train_loader, val_loader, epochs = 20, device = "gpu"):
    for epoch in range(epochs):
        training_loss = 0.0
        valid_loss = 0.0
        model.train()
    
        for batch in train_loader:
            optimizer.zero_grad()
            inputs, target = (torch.reshape(batch['mix'], (1,1,-1)), torch.reshape(batch['target'], (1,2,-1)))
            inputs = inputs.to(device)
            target = torch.tensor(target).to(device)
            print(inputs.shape)
            output = model(inputs)
            loss = loss_fn(output, target)
            loss.backward()
            optimizer.step()
            training_loss += loss.data.item() * inputs.size(0)
        training_loss /= len(train_loader.dataset)

        model.eval()
        num_correct = 0
        num_examples = 0
        for batch in val_loader:
            inputs, targets = batch
            inputs = inputs.to(device)
            outputs = model(inputs)
            targets = targets.to(device)
            loss = loss_fn(outputs, targets)
            valid_loss += loss.data.item() * inputs.size(0)
            correct = torch.eq(torch.max(F.softmax(output), dim = 1)[1], target).view[-1]
            num_correct +=torch.sum(correct).item()
            num_examples += correct.shape[0]
        valid_loss /= len(val_loader.dataset)

        print(f'Epoch = {epoch}, Training Loss = {np.round(training_loss, 2)}')
        print(f'Validation loss = {np.round(valid_loss, 2)}, Accuracy = {np.round(num_correct/num_examples, 2)}')

train_size = int(0.8 * len(full_dataset))
test_size = len(full_dataset) - train_size
train_dataset, test_dataset = torch.utils.data.random_split(full_dataset, [train_size, test_size])
train_loader = DataLoader(train_dataset, batch_size = 1, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size = 1, shuffle=True)
val_loader = DataLoader(test_dataset, batch_size = 1, shuffle=True)
loss_fn = torch.nn.MSELoss()

import torch
torch.cuda.empty_cache()
train(model, optimizer, loss_fn, train_loader, val_loader, epochs = 1, device = "cuda")