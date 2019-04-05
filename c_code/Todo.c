#include<stdio.h>

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
    printf("%s\n", buf);
    return 0;
}

static int
rule_index_num_get(char *rule_name)
{
    char *cmdbuf, *tmp; // use array or pointer... define max rule name?
    char output[1024];
    int index;

    sprintf(cmdbuf, "uci show firewall | grep %s", rule_name);
    if (!(read_shell_output(*cmdbuf, *output)) < 0){
        printf("error reading shell output\n");
        return (-1);
    }
    sscanf(output, "firewall.@redirect[%d]", &index);// error index 0... 

    return index;
}
