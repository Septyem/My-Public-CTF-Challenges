// put this file at binutils-2.43.1/chal dir
// gcc -Wl,-z,relro,-z,now -O3 not_linker.c -o not_linker -I ../include/ -lz -lzstd  ../bfd/.libs/libbfd.a ../libiberty/libiberty.a ../libsframe/.libs/libsframe.a

#include "../bfd/sysdep.h"
#include "../bfd/bfd.h"
#include "../bfd/libbfd.h"

#include "bfdlink.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

FILE *fp;
int debug = 0;
void *regs[0x101];

uint8_t getinput() {
    int x = 0;
    if (!debug) {
        fread(&x, 1, 1, fp);
    } else {
        printf("> ");
        scanf("%d", &x);
    }
    return x;
}

void getbuf(uint8_t *buf) {
    for (int i=0; i<8; i++) {
        uint8_t x = getinput();
        buf[i] = x;
        if (!x) {
            break;
        }
    }
    buf[8] = 0;
}

bfd *open_bfd(const char *filename) {
    bfd *abfd;

    bfd_init();
    abfd = bfd_openr(filename, NULL);
    if (!abfd) {
        return NULL;
    }
    if (!bfd_check_format(abfd, bfd_object)) {
        return NULL;
    }

    return abfd;
}

int main(int argc, char**argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s [filename] | debug\n", argv[0]);
        return EXIT_FAILURE;
    }
    if (strcmp(argv[1], "debug")) {
       fp = fopen(argv[1], "rb");
       if (!fp) {
           perror("no file found");
           return EXIT_FAILURE;
       }
    } else if (strcmp(argv[1], "aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaac")) {
        perror("Not pwn me :(\nplay with object files should be much easier\n");
        return EXIT_FAILURE;
    } else {
        debug = 1;
    }

    regs[0] = (void *)open_bfd("a.o");
    regs[1] = (void *)open_bfd("b.o");
    regs[2] = (void *)bfd_openw("out.o", bfd_get_target((bfd*)regs[0]));
    uint8_t c, a0, a1, a2, a3, a4, a5;
    uint8_t buf[10];
    while (1) {
        uint8_t c = getinput();
        if (c==0) {
            bfd_close(regs[2]);
            break;
        } else if (c==1) {
            a0 = getinput();
            a1 = getinput();
            asection *sec = (asection *)regs[a1];
            regs[a0] = (void*)bfd_section_name(sec);
        } else if (c==2) {
            a0 = getinput();
            a1 = getinput();
            asection *sec = (asection *)regs[a1];
            regs[a0] = (void*)bfd_section_size(sec);
        } else if (c==3) {
            a0 = getinput();
            a1 = getinput();
            asection *sec = (asection *)regs[a1];
            regs[a0] = (void*)bfd_section_vma(sec);
        } else if (c==4) {
            a0 = getinput();
            a1 = getinput();
            asection *sec = (asection *)regs[a1];
            regs[a0] = (void*)bfd_section_lma(sec);
        } else if (c==5) {
            a0 = getinput();
            a1 = getinput();
            asection *sec = (asection *)regs[a1];
            regs[a0] = (void*)bfd_section_alignment(sec);
        } else if (c==6) {
            a0 = getinput();
            a1 = getinput();
            asection *sec = (asection *)regs[a1];
            regs[a0] = (void*)bfd_section_flags(sec);
        } else if (c==7) {
            a0 = getinput();
            a1 = getinput();
            asection *sec = (asection *)regs[a1];
            regs[a0] = (void*)bfd_section_userdata(sec);
        } else if (c==8) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            asection *sec = (asection *)regs[a1];
            regs[a0] = (void*)bfd_set_section_userdata(sec, regs[a2]);
        } else if (c==9) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            asection *sec = (asection *)regs[a1];
            bfd_vma vma = (bfd_vma)regs[a2];
            regs[a0] = (void*)bfd_set_section_vma(sec, vma);
        } else if (c==10) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            asection *sec = (asection *)regs[a1];
            bfd_vma lma = (bfd_vma)regs[a2];
            regs[a0] = (void*)bfd_set_section_lma(sec, lma);
        } else if (c==11) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            asection *sec = (asection *)regs[a1];
            regs[a0] = (void*)bfd_set_section_alignment(sec, a2);
        } else if (c==12) {
            a0 = getinput();
            a1 = getinput();
            getbuf(buf);
            bfd *abfd = (bfd *)regs[a1];
            regs[a0] = (void*)bfd_get_section_by_name(abfd, buf);
        } else if (c==13) {
            a0 = getinput();
            a1 = getinput();
            getbuf(buf);
            bfd *abfd = (bfd *)regs[a1];
            regs[a0] = (void*)bfd_get_linker_section(abfd, buf);
        } else if (c==14) {
            a0 = getinput();
            a1 = getinput();
            getbuf(buf);
            bfd *abfd = (bfd *)regs[a1];
            regs[a0] = (void*)bfd_make_section_old_way(abfd, buf);
        } else if (c==15) {
            a0 = getinput();
            a1 = getinput();
            getbuf(buf);
            a2 = getinput();
            bfd *abfd = (bfd *)regs[a1];
            flagword flags = (flagword)regs[a2];
            regs[a0] = (void*)bfd_make_section_with_flags(abfd, buf, flags);
        } else if (c==16) {
            a0 = getinput();
            a1 = getinput();
            getbuf(buf);
            bfd *abfd = (bfd *)regs[a1];
            regs[a0] = (void*)bfd_make_section(abfd, buf);
        } else if (c==17) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            asection *sec = (asection *)regs[a1];
            bfd_size_type val = (bfd_size_type)regs[a2];
            regs[a0] = (void*)bfd_set_section_size(sec, val);
        } else if (c==18) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            a3 = getinput();
            a4 = getinput();
            a5 = getinput();
            bfd *abfd = (bfd *)regs[a1];
            asection *sec = (asection *)regs[a2];
            const void *data = (const void *)regs[a3];
            regs[a0] = (void*)bfd_set_section_contents(abfd, sec, data, a4, a5);
        } else if (c==19) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            a3 = getinput();
            a4 = getinput();
            a5 = getinput();
            bfd *abfd = (bfd *)regs[a1];
            asection *sec = (asection *)regs[a2];
            void *data = (void *)regs[a3];
            regs[a0] = (void*)bfd_get_section_contents(abfd, sec, data, a4, a5);
        } else if (c==20) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            a3 = getinput();
            a4 = getinput();
            bfd *ibfd = (bfd *)regs[a1];
            asection *isec = (asection *)regs[a2];
            bfd *obfd = (bfd *)regs[a3];
            asection *osec = (asection *)regs[a4];
            regs[a0] = (void*)bfd_copy_private_section_data(ibfd, isec, obfd, osec);
        } else if (c==21) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            bfd *abfd = (bfd *)regs[a1];
            asymbol *ptrs[2];
            ptrs[0] = regs[a2];
            ptrs[1] = 0;
            regs[a0] = (void*)bfd_set_symtab(abfd, ptrs, 1);
        } else if (c==22) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            a3 = getinput();
            getbuf(buf);
            asymbol *sym = (asymbol *)regs[a0];
            asection *sec = (asection *)regs[a1];
            sym->section = sec;
            sym->flags = a2;
            sym->value = a3;
            sym->name = strdup(buf);
        } else if (c==23) {
            a0 = getinput();
            a1 = getinput();
            bfd *abfd = (bfd *)regs[a1];
            regs[a0] = (void*)bfd_make_empty_symbol(abfd);
        } else if (c==24) {
            a0 = getinput();
            a1 = getinput();
            bfd *abfd = (bfd *)regs[a1];
            asymbol *sym = (asymbol *)regs[a1];
            regs[a0] = (void*)bfd_decode_symclass(sym);
        } else if (c==25) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            a3 = getinput();
            a4 = getinput();
            bfd *ibfd = (bfd *)regs[a1];
            asymbol *isym = (asymbol *)regs[a2];
            bfd *obfd = (bfd *)regs[a3];
            asymbol *osym = (asymbol *)regs[a4];
            regs[a0] = (void*)bfd_copy_private_symbol_data(ibfd, isym, obfd, osym);
        } else if (c==26) {
            a0 = getinput();
            a1 = getinput();
            bfd *abfd = (bfd *)regs[a0];
            const bfd_arch_info_type *arg = (const bfd_arch_info_type *)regs[a1];
            bfd_set_arch_info(abfd, arg);
        } else if (c==27) {
            a0 = getinput();
            a1 = getinput();
            bfd *abfd = (bfd *)regs[a1];
            regs[a0] = (void*)bfd_get_arch_info(abfd);
        } else if (c==28) {
            a0 = getinput();
            a1 = getinput();
            bfd *abfd = (bfd *)regs[a1];
            regs[a0] = (void*)bfd_get_format(abfd);
        } else if (c==29) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            bfd *abfd = (bfd *)regs[a1];
            bfd_format format = (bfd_format)regs[a2];
            regs[a0] = (void*)bfd_set_format(abfd, format);
        } else if (c==30) {
            a0 = getinput();
            a1 = getinput();
            asymbol *sym = (asymbol *)regs[a1];
            regs[a0] = (void*)bfd_asymbol_section(sym);
        } else if (c==31) {
            a0 = getinput();
            a1 = getinput();
            asymbol *sym = (asymbol *)regs[a1];
            regs[a0] = (void*)bfd_asymbol_value(sym);
        } else if (c==32) {
            a0 = getinput();
            a1 = getinput();
            asymbol *sym = (asymbol *)regs[a1];
            regs[a0] = (void*)bfd_asymbol_name(sym);
        } else if (c==33) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            bfd *ibfd = (bfd *)regs[a1];
            bfd *obfd = (bfd *)regs[a2];
            regs[a0] = (void*)bfd_copy_private_header_data(ibfd, obfd);
        } else if (c==34) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            bfd *ibfd = (bfd *)regs[a1];
            bfd *obfd = (bfd *)regs[a2];
            regs[a0] = (void*)bfd_copy_private_bfd_data(ibfd, obfd);
        } else if (c==35) {
            a0 = getinput();
            a1 = getinput();
            a2 = getinput();
            bfd *abfd = (bfd *)regs[a1];
            asection *sec = (asection *)regs[a2];
            regs[a0] = (void*)bfd_link_split_section(abfd, sec);
        }
    }
    return 0;
}
