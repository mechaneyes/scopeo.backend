# Scopeo

### Experiments in Computer Vision

<br><br>


# Local Machine

## File System Packages

If you want to inherit the currently installed packages from the system Python, you should create your virtual environment using python -m venv --system-site-packages env.

```bash
python -m venv --system-site-packages .venv
```

## (Un)Mount Network Shares

https://www.linode.com/docs/guides/linux-mount-smb-share/

### Mount

```bash
sudo mount -t cifs -o credentials=CREDENTIALSFILE,uid=UID,gid=GID,dir_mode=0744,file_mode=0744 //FILESERVER/project /mnt/project
```

### Verify Mounted Shares

```bash
mount -t cifs
```

### Unmount

```bash
umount /mnt
```

# Soundtrack

A running list of albums, tracks and sets that have accompanied me while working on this project.

### Michael Mayer - All Night Long at Gewölbe Cologne (Nov 2023)
https://soundcloud.com/michael-mayer-kompakt/gewoelbeallnightlong

### Frank & Tony (Vinyl Set) - Robot Heart Residency - Oakland 2023
https://soundcloud.com/robot-heart/frank_tony_vinyl_set_robot_heart_residency_oakland_2023

