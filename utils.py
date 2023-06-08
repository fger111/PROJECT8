import torch
import torchvision.transforms as transforms
from PIL import Image


def print_examples(model, device, dataset):
    transform = transforms.Compose(
        [
            transforms.Resize((299, 299)),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
    )

    model.eval()
    test_img1 = transform(Image.open("test_examples/colon.jpg").convert("RGB")).unsqueeze(
        0
    )
    print("Example 1 CORRECT: Colon Polyp")
    print(
        "Example 1 OUTPUT: "
        + " ".join(model.caption_image(test_img1.to(device), dataset.vocab))
    )
    test_img2 = transform(
        Image.open("test_examples/colon_2.jpg").convert("RGB")
    ).unsqueeze(0)
    print("Example 2 CORRECT: Colon Polyp")
    print(
        "Example 2 OUTPUT: "
        + " ".join(model.caption_image(test_img2.to(device), dataset.vocab))
    )
    test_img3 = transform(Image.open("test_examples/colon_3.jpg").convert("RGB")).unsqueeze(
        0
    )
    print("Example 3 CORRECT: Colon Polyp")
    print(
        "Example 3 OUTPUT: "
        + " ".join(model.caption_image(test_img3.to(device), dataset.vocab))
    )
    test_img4 = transform(Image.open("test_examples/colon_4.jpg").convert("RGB")).unsqueeze(
        0
    )
    print("Example 4 CORRECT: Diverticular")
    print(
        "Example 4 OUTPUT: "
        + " ".join(model.caption_image(test_img4.to(device), dataset.vocab))
    )
    test_img5 = transform(Image.open("test_examples/colon_5.jpg").convert("RGB")).unsqueeze(
        0
    )
    print("Example 5 CORRECT: Diverticular")  # Add this line to check the shape of img
    print(
        "Example 5 OUTPUT: "
        + " ".join(model.caption_image(test_img5.to(device), dataset.vocab))
    )
    test_img6 = transform(Image.open("test_examples/colon_6.jpg").convert("RGB")).unsqueeze(
        0
    )
    print("Example 6 CORRECT: Diverticular")
    print(
        "Example 6 OUTPUT: "
        + " ".join(model.caption_image(test_img6.to(device), dataset.vocab))
    )
    model.train()

def save_checkpoint(state, filename="my_checkpoint.pth"):
    print("=> Saving checkpoint")
    torch.save(state, filename)


def load_checkpoint(checkpoint, model, optimizer):
    print("=> Loading checkpoint")
    model.load_state_dict(checkpoint["state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer"])
    step = checkpoint["step"]
    return step
