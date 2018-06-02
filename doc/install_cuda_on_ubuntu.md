安装 Nvidia driver 时，只安装驱动，不安装 OpenGL 文件（即桌面显示不利用N卡，在跑程序时最大程度利用显存）。
```sh
sudo sh ./NVIDIA-Linux-x86_64-390.48.run -no-x-check -no-nouveau-check -no-opengl-files
```