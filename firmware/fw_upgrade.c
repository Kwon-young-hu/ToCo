#include<stdio.h>
#include<unistd.h>
#include<stdlib.h>
#include<string.h>

#include "uci_conf.h"

static int
read_shell_output(char *cmd, char *buf)
{
    FILE    *fp =NULL;
    size_t  readSize = 0;

    fp = popen(cmd, "r");
    if (!fp){
        printf("popen fail\n");
        return (-1);
    }
    readSize = fread(buf, sizeof(char), 1024-1, fp);
    if (readSize == 0){
        pclose(fp);
        printf("output file size 0, please check to output\n");
        return (-1);
    }
    pclose(fp);
    return 0;
}

static int
eval(char *cmd)
{
    int status;
    status = system(cmd);
    
    if (WEXITSTATUS(status)){
        printf("%s result = %d\n",cmd, WEXITSTATUS(status));
        return WEXITSTATUS(status);
    }
    else{
        printf("system call fail\n");
        return(-1);   
    }
}

static int 
tftp_image_download(char *filename, char *serverip)
{
    char cmdbuf[128];
    int result = chdir("/tmp");

    if (result != 0){
        printf("**Directory move failed**\n");
        return (-1);
    }
    sprintf(cmdbuf, "tftp -gr %s %s", filename, serverip);
    printf("%s\n",cmdbuf);
    return 0;//eval(cmdbuf);
}

static int 
nand_flash_erase(char *mtd_part)
{
    char strbuf[64];

    sprintf(strbuf,"flash_erase %s 0 0", mtd_part);
    printf("%s\n",strbuf);
    return 0;//eval(strbuf);
}

static int 
nand_flash_write(char *mtd_part, char *img)
{
    char strbuf[64];

    sprintf(strbuf,"nandwrite %s -p %s", mtd_part, img);
    printf("%s\n",strbuf);
    return 0;//eval(strbuf);    
}

static int 
active_part_get(char *mtd_part)
{
    int part_num;
    char strbuf[64];

    if (read_shell_output("fw_printenv active_part", strbuf) != 0){
        printf("active_part_get error\n");
        return (-1);
    }
    sscanf(strbuf,"active_part=%d", &part_num);

    switch(part_num){
        case 0 :
            part_num = 1;
            strcpy(mtd_part,"/dev/mtd3");
            break;
        case 1 :
            part_num = 0;
            strcpy(mtd_part,"/dev/mtd2");
            break;
        default :
            part_num = -1;
            break;
    }
    return part_num;
}

int main(void)
{
    int  part_num;
    char mtd_part[16];
    char filename[32];
    char serverip[32];
    char type[16];
    char cmdbuf[64];

    config_get("system.upgrade.filename", filename, sizeof(filename));
    config_get("system.upgrade.server", serverip, sizeof(serverip));
    config_get("system.upgrade.type", type, sizeof(type));

    if (tftp_image_download(filename, serverip) != 0){
        printf("download image error\n");
        return (-1);
    }
    if ((part_num = active_part_get(mtd_part)) == -1){
        printf("not found active part \n");
        return (-1);
    }
    if (nand_flash_erase(mtd_part) != 0){
        printf("nand flash erase fail \n");
        return (-1);
    }
    if (nand_flash_write(mtd_part, filename) != 0){
        printf("nand_flash_write fail \n");
        return (-1); 
    }
    sprintf(cmdbuf,"fw_setenv active_part %d", part_num);
    printf("%s\n",cmdbuf);
    /*if (eval(cmdbuf) !=0){
      printf("active_part set error\n");
      return (-1);
      }*/

    return 0;
}


/*
static int 
mtd_part_get(int part_num, char *mtd_part)
{
    switch (part_num) {
        case 0 : strcpy(mtd_part, "/dev/mtd3"); break;
        case 1 : strcpy(mtd_part, "/dev/mtd2"); break;
        default : return (-1);
    }
    return 0;
}*/

/*
    switch(part_num){
        case 0 :
            if (system("fw_setenv active_part 1") !=0){
                printf("active_part set error\n");
                return (-1);
            }
            printf("fw_setenv active_part 1\n");
            break;
        case 1 : 
            if (system("fw_setenv active_part 0") !=0){
                printf("active_part set error\n");
                return (-1);
            }
            printf("fw_setenv active_part 0\n");
            break;
        default : 
            return (-1);
    }
    return 0;*/
