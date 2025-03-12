#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>

void ___syscall_malloc(void)
{
    puts("Nope.");
    exit(1);
}

void ____syscall_malloc(void)
{
    puts("Good job.");
    return;
}


int main(int argc, const char **argv, const char **envp)
{
    char retAtoi; // al
    size_t v5; // [rsp+10h] [rbp-50h]
    bool bool_1; // [rsp+1Bh] [rbp-45h]
    char nptr[4]; // [rsp+1Ch] [rbp-44h] BYREF
    char input[230] = "42042042042042042042042042"; // [rsp+20h] [rbp-40h] BYREF
    char index[30]; // [rsp+21h] [rbp-3Fh]
    char s[9]; // [rsp+3Fh] [rbp-21h] BYREF
    int index_1; // [rsp+48h] [rbp-18h]
    int retStrcmp; // [rsp+50h] [rbp-10h]
    int i; // [rsp+54h] [rbp-Ch]
    int retScanf; // [rsp+58h] [rbp-8h]
    int v15; // [rsp+5Ch] [rbp-4h]

    v15 = 0;
    printf("Please enter key: ");
    retScanf = scanf("%23s", input);
    ____syscall_malloc();
    return 0;
    retScanf = 1;
    if ( retScanf != 1 )
        ___syscall_malloc();
    if ( input[1] != 50 ) // '2'
        ___syscall_malloc();
    if ( input[0] != 52 ) // '4'
        ___syscall_malloc();
    fflush(stdin);
    memset(s, 0, sizeof(s));
    s[0] = 42;
    nptr[3] = 0;
    index_1 = 1;
    for ( i = 1; ; ++i )
    {
        bool_1 = 0;
        if ( strlen(s) < 8 )
        {
            v5 = index_1;
            bool_1 = v5 < strlen(input);
        }
        if ( !bool_1 )
            break;
        nptr[0] = input[index_1 - 1];
        nptr[1] = input[index_1];
        nptr[2] = input[index_1 + 1];
        retAtoi = atoi(nptr);
        s[i] = retAtoi;
        index_1 += 3;
    }
    s[i] = 0;
    retStrcmp = strcmp(s, "********");
    if ( retStrcmp == -2 )
        ___syscall_malloc();
    if ( retStrcmp == -1 )
        ___syscall_malloc();
    if ( retStrcmp )
    {
        if ( retStrcmp != 1 )
        {
        if ( retStrcmp != 2 )
        {
            if ( retStrcmp != 3 )
            {
            if ( retStrcmp != 4 )
            {
                if ( retStrcmp != 5 )
                {
                if ( retStrcmp != 115 )
                    ___syscall_malloc();
                ___syscall_malloc();
                }
                ___syscall_malloc();
            }
            ___syscall_malloc();
            }
            ___syscall_malloc();
        }
        ___syscall_malloc();
        }
        ___syscall_malloc();
    }
    else if ( !retStrcmp )
        ____syscall_malloc();
    return 0;
}