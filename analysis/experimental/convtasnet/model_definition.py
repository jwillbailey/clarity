import torch
import torchaudio
import torch.nn.functional as F
import numpy as np
from torchaudio.models import ConvTasNet as ctn

model = ctn()

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

model = model.to(device)


optimizer = torch.optim.Adam(model.parameters(), lr=0.001)


def train(model, optimizer, loss_fn, train_loader, val_loader, epochs = 20, device = "cpu"):
    for epoch in range(epochs):
        training_loss = 0.0
        valid_loss = 0.0
        model.train()
    
        for batch in train_loader:
            optimizer.zero_grad()
            inputs, target = batch
            inputs = inputs.to(device)
            targets = targets.to(device)
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
            loss = loss_fn(output, targets)
            valid_loss += loss.data.item() * inputs.size(0)
            correct = torch.eq(torch.max(F.softmax(output), dim = 1)[1], target).view[-1]
            num_correct +=torch.sum(correct).item()
            num_)examples += correct.shape[0]
        valid_loss /= len(val_loader.dataset)

        print(f'Epoch = {epoch}, Training Loss = {np.round(training_loss, 2)}')
        print(f'Validation loss = {np.round(valid_loss, 2)}, Accuracy = {np.round(num_correct/num_examples, 2)}')

