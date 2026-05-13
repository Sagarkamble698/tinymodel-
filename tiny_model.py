import torch
import torch.nn as nn
import torch.optim as optim

# -----------------------
# 1. Load Data
# -----------------------
text = "AI is the future. AI is powerful."

chars = sorted(set(text))
stoi = {c:i for i,c in enumerate(chars)}
itos = {i:c for c,i in stoi.items()}

data = torch.tensor([stoi[c] for c in text], dtype=torch.long)

vocab_size = len(chars)

# -----------------------
# 2. Model
# -----------------------
class TinyLLM(nn.Module):
    def __init__(self):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, 16)
        self.rnn = nn.GRU(16, 32, batch_first=True)
        self.fc = nn.Linear(32, vocab_size)

    def forward(self, x):
        x = self.embed(x)
        out, _ = self.rnn(x)
        return self.fc(out)

model = TinyLLM()

# -----------------------
# 3. Training
# -----------------------
optimizer = optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.CrossEntropyLoss()

seq_len = 10

for step in range(200):
    i = torch.randint(0, len(data)-seq_len, (1,))
    x = data[i:i+seq_len].unsqueeze(0)
    y = data[i+1:i+seq_len+1].unsqueeze(0)

    out = model(x)
    loss = loss_fn(out.view(-1, vocab_size), y.view(-1))

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if step % 50 == 0:
        print("Loss:", loss.item())

# -----------------------
# 4. Generate Text
# -----------------------
def generate(start="A", length=50):
    x = torch.tensor([[stoi.get(c, 0) for c in start]])

    for _ in range(length):
        out = model(x)
        probs = torch.softmax(out[0, -1], dim=0)
        idx = torch.multinomial(probs, 1).item()
        x = torch.cat([x, torch.tensor([[idx]])], dim=1)

    return "".join([itos[i] for i in x[0]])

print("\nGenerated Text:\n")
print(generate("AI"))