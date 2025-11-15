import torch
import torch.nn as nn
import torchvision.models as models

#ResNet50 - model preantrenat pentru extragere de feature din imagini
class ResNet50Backbone(nn.Module):
    def __init__(self):
        super().__init__()
        base_model = models.resnet50(pretrained=True)
        self.backbone = nn.Sequential(*list(base_model.children())[:-2])  

    def forward(self, x):
        return self.backbone(x)

#MammoTransformerHead - partea de Vision Transformer care proceseaza feature-urile de CNN
class MammoTransformerHead(nn.Module):
    def __init__(self, input_channels=2048, embed_dim=768, num_heads=6, num_layers=4, num_patches=49):  # 7x7
        super().__init__()
        self.embedding = nn.Conv2d(input_channels, embed_dim, kernel_size=1)
        self.cls_token = nn.Parameter(torch.randn(1, 1, embed_dim))
        self.pos_embed = nn.Parameter(torch.randn(1, num_patches + 1, embed_dim))  # <-- moved here

        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, batch_first=True),
            num_layers=num_layers
        )

        self.fc = nn.Linear(embed_dim, 2)

    def forward(self, x):  
        x = self.embedding(x) 
        B, C, H, W = x.shape
        x = x.flatten(2).transpose(1, 2) 

        cls_token = self.cls_token.expand(B, -1, -1) 
        x = torch.cat([cls_token, x], dim=1)  

        x = x + self.pos_embed
        x = self.transformer(x)
        return self.fc(x[:, 0])

#MammoVit - combinatie intre ResNet50 si MammoTransformerHead care ne ofera diagnostic de malign sau benign
class MammoVit(nn.Module):
    def __init__(self):
        super().__init__()
        self.backbone = ResNet50Backbone()
        self.head = MammoTransformerHead()

    def forward(self, x):
        feats = self.backbone(x)        
        logits = self.head(feats)        
        return logits
