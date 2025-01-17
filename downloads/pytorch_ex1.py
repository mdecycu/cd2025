# pip install numpy torch
# related to https://arxiv.org/pdf/2405.20592 (Contrastive Learning for Mechanism Synthesis)
# 利用對比學習訓練四連桿通過特定點
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import numpy as np

def four_bar_mechanism_with_triangle(x1, x2, x3, x4, theta):
    """
    計算四連桿機構上三角形頂點的位置
    """
    l1, l2, l3, l4 = x1, x2, x3, x4
    
    x = l1 * np.cos(theta) + l2 * np.cos(np.pi - theta)
    y = l1 * np.sin(theta) + l2 * np.sin(np.pi - theta)
    
    triangle_x = [x + l3 * np.cos(np.pi / 3), x - l3 * np.cos(np.pi / 3), x]
    triangle_y = [y + l3 * np.sin(np.pi / 3), y - l3 * np.sin(np.pi / 3), y]
    
    return triangle_x, triangle_y

class MechanismDataset(Dataset):
    def __init__(self, num_samples=1000, num_points=100):
        self.num_samples = num_samples
        self.num_points = num_points
        self.data = []
        
        for _ in range(num_samples):
            x1, x2, x3, x4 = np.random.uniform(1, 10, size=4)
            theta = np.linspace(0, 2*np.pi, num_points)
            
            trajectory = []
            for t in theta:
                triangle_x, triangle_y = four_bar_mechanism_with_triangle(x1, x2, x3, x4, t)
                trajectory.extend([np.mean(triangle_x), np.mean(triangle_y)])
            
            self.data.append((
                torch.tensor([x1, x2, x3, x4], dtype=torch.float32),
                torch.tensor(trajectory, dtype=torch.float32)
            ))
    
    def __len__(self):
        return self.num_samples
    
    def __getitem__(self, idx):
        return self.data[idx]

class ContrastiveLoss(nn.Module):
    def __init__(self, margin=1.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin
    
    def forward(self, output1, output2, label):
        euclidean_distance = F.pairwise_distance(output1, output2)
        loss = torch.mean((1 - label) * torch.pow(euclidean_distance, 2) +
                         label * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))
        return loss

class MechanismNetwork(nn.Module):
    def __init__(self, input_dim=4, hidden_dim=256, embedding_dim=128):
        super(MechanismNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.fc3 = nn.Linear(hidden_dim // 2, embedding_dim)
        
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.bn2 = nn.BatchNorm1d(hidden_dim // 2)
        
        self.dropout = nn.Dropout(0.3)
        
    def forward(self, x):
        x = F.relu(self.bn1(self.fc1(x)))
        x = self.dropout(x)
        x = F.relu(self.bn2(self.fc2(x)))
        x = self.dropout(x)
        x = self.fc3(x)
        return F.normalize(x, p=2, dim=1)

def calculate_similarity(trajectory1, trajectory2):
    """
    計算兩個軌跡的相似度（修正版）
    """
    # 首先確保資料是正確的形狀
    trajectory1 = trajectory1.view(-1)  # 展平為一維向量
    trajectory2 = trajectory2.view(-1)  # 展平為一維向量
    
    # 計算歐氏距離
    distance = torch.norm(trajectory1 - trajectory2)
    
    # 使用距離計算相似度分數
    similarity = torch.exp(-distance / distance.mean())
    
    return similarity

def train_model(model, dataset, batch_size=64, num_epochs=10, lr=0.001, similarity_threshold=0.5):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    model = model.to(device)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    criterion = ContrastiveLoss(margin=1.0)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=3)
    
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        num_batches = 0
        
        for batch in dataloader:
            optimizer.zero_grad()
            
            mechanism_params, trajectories = batch
            mechanism_params = mechanism_params.to(device)
            trajectories = trajectories.to(device)
            
            batch_size = mechanism_params.size(0)
            if batch_size < 2:
                continue
                
            embeddings = model(mechanism_params)
            
            loss = 0
            num_pairs = 0
            for i in range(0, batch_size-1, 2):
                similarity = calculate_similarity(trajectories[i], trajectories[i+1])
                label = (similarity > similarity_threshold).float()
                
                pair_loss = criterion(
                    embeddings[i].unsqueeze(0),
                    embeddings[i+1].unsqueeze(0),
                    label.unsqueeze(0).to(device)
                )
                loss += pair_loss
                num_pairs += 1
            
            if num_pairs > 0:
                loss = loss / num_pairs
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()
                
                total_loss += loss.item()
                num_batches += 1
        
        avg_loss = total_loss / num_batches if num_batches > 0 else 0
        print(f"Epoch [{epoch+1}/{num_epochs}], Average Loss: {avg_loss:.4f}")
        
        scheduler.step(avg_loss)
    
    return model

def main():
    torch.manual_seed(42)
    np.random.seed(42)
    
    dataset = MechanismDataset(num_samples=1000, num_points=100)
    
    model = MechanismNetwork(
        input_dim=4,
        hidden_dim=256,
        embedding_dim=128
    )
    
    trained_model = train_model(
        model=model,
        dataset=dataset,
        batch_size=64,
        num_epochs=50,
        lr=0.001,
        similarity_threshold=0.5
    )
    
    torch.save(trained_model.state_dict(), 'mechanism_model.pth')
    print("Training completed and model saved.")

if __name__ == "__main__":
    main()