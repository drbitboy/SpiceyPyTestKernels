
N00NN=n0066
FINAL_C=spkpvn.c
ORIGINAL=$(FINAL_C).$(N00NN).original
PATCHFILE=$(ORIGINAL:%.$(N00NN).original=%.patch)

all: $(FINAL_C)

$(FINAL_C): $(ORIGINAL) $(PATCHFILE)
	$(RM) $@
	cp $(ORIGINAL) $@
	patch $@ $(PATCHFILE)

clean:
	$(RM) $(FINAL_C)
