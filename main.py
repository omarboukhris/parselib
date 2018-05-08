from lexlib import grammarparser as gp, graphbuilder as gb

txtgrammar = """
AXIOM := S
S     	 := 
	'cc' A A
A := 
	'aa' B B |
	''
B :=
	'bb' |
	'xx' |
	C
C := 
	'cc' |
	''
"""

if __name__ == '__main__':
	#TEST_RUN
	grammartokens = [
		('AXIOM',			'AXIOM'),
		('[a-zA-Z_]\w*',	'NONTERMINAL'),
		('\'.*\'',			'TERMINAL'),
		('\:=',				'EQUAL'),
		('\|',				'OR'),
		('\'\'',			'EMPTY'),
	]
	
	AXIOM = r'AXIOM EQUAL NONTERMINAL'
	LSIDE = r'NONTERMINAL EQUAL'
	RSIDE = r'(TERMINAL|NONTERMINAL)+|EMPTY '
	OR = r'OR'
	genericgrammarprodrules = [
		(AXIOM, 'AXIOM'),
		(LSIDE, 'LSIDE'),
		(RSIDE, 'RSIDE'),
		(OR,	'OR'),
	]

	#lex language => tokenized grammar
	tokenizer = gp.Tokenizer (grammartokens)
	tokenizer.parse (txtgrammar)
	print(tokenizer)
	
	#lex tokenized grammar => tokenized language
	gram = gp.GenericGrammarParser (genericgrammarprodrules)
	gram.parse (tokenizer)
	print(gram)

	#make production rules
	prodrulesgen = gp.ProductionRulesGenerator ()
	prodrulesgen.makeprodrules (
		gram.tokenizedgrammar,
		tokenizer.tokenizedgrammar,
	)
	print (prodrulesgen)
	prodrulesgen.save("blob.pkl")
	prodrulesgen.load("blob.pkl")
	
	#graph generator goes here
	gg = gb.GraphGenerator (prodrulesgen.production_rules)
	axiom = gg.buildgraph()
	print (axiom)
	