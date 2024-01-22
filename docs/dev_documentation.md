# Steps performed to create this project

* Used Git Codespace to develop this project [Video Reference](https://www.youtube.com/watch?v=XOSUt8Ih3zA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=15)
* Connected Git Codespace to local VSCode
* Git Codespace server already has installed the following:
    * docker
    * conda
    * python
* Created a virtual conda environment 
    ```bash
       conda create --prefix ./.my_env python=3.9.1 pip 
       conda init
       cd ~
       source .bashrc
       cd /workspaces/ny_taxi/
       conda activate .my_env
    ```
* Updated `.gitignore` file

## Starting development - Steps

* Activate conda virtual env
* 