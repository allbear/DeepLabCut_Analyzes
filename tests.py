import torch
model = torch.hub.load('.', model='custom', path='Cinderella.pt', source='local')
img = "images/idol.jpg"
results = model(img)
results.show()
