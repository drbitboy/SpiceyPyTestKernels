
N00NN=n0066
FINAL_C=spkpvn.c
ORIGINAL=$(FINAL_C:%=%.$(N00NN).original)
PATCHFILE=$(ORIGINAL:%.$(N00NN).original=%.patch)

all: $(FINAL_C)

%.c: %.c.n0066.original %.c.patch
	$(RM) $@
	cp $< $@
	patch $@ $@.patch

clean:
	$(RM) $(FINAL_C)
