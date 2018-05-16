from suffix_classifier import SuffixClassifier

st = SuffixClassifier("ab1bc1bb0ba0$")
st.print_suffix_tree()
st.truncate_tree()
st.print_suffix_tree()
st.recalculate(0)
st.print_suffix_tree()
