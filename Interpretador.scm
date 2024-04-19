#lang eopl


;******************************************************************************************
;;;;; Interpretador para lenguaje con condicionales, ligadura local, procedimientos y 
;;;;; procedimientos recursivos
;;olaaaaaa
;; La definición BNF para las expresiones del lenguaje:
;;
;;  <programa>      ::= <expresion>
;;                      <un-programa (exp)>
;;  <expresion>     ::= <numero>
;;                      <numero-lit (num)>
;;                  ::= "\""texto<>"\""
;;                      <texto-lit(txt)>
;;                  ::= <identificador>
;;                      <var-exp (id)>
;;                  ::= (<expresion> <primitiva-binaria> <expresion>)
;;                      <primapp-bin-exp (prim-unaria rands)>
;;                  ::= <primitiva-unaria> ({<expresion>}*(,))
;;                      <primapp-exp (prim-unaria rands)>
;;                  ::= if <expresion> then <expresion> else <expresion>
;;                      <condicional-exp (exp1 exp2 exp23)>
;;                  ::= let {identificador = <expresion>}* in <expresion>
;;                      <variableLocal-exp (ids rands body)>
;;                  ::= proc({<identificador>}*(,)) <expresion>
;;                      <procedimiento-ex (ids body)>
;;                  ::= (<expresion> {<expresion>}*)
;;                      <app-exp proc rands>
;;                  ::= letrec  {identificador ({identificador}*(,)) = <expresion>}* in <expresion>
;;                     <letrec-exp proc-names idss bodies bodyletrec>
;;  <primitiva-binaria>   ::= | + | ~  | * | / | concat |
;;  <primitiva-unaria>    ::= | longitud | add1 () | sub1 |

;******************************************************************************************

;******************************************************************************************
;Especificación Léxica

(define scanner-spec-simple-interpreter
'((white-sp
   (whitespace) skip)
  (comment
   ("%" (arbno (not #\newline))) skip)
  (numero
   (digit (arbno digit)) number)
  (numero
   (digit (arbno digit) "." digit (arbno digit)) number)
  (numero
   ("-" digit (arbno digit) "." digit (arbno digit)) number)
  (numero
   ("-" digit (arbno digit)) number)
  
  (identificador
   ("@" letter (arbno (or letter digit "?"))) symbol)

  (texto
   ("\"" any "\"") string)

  ))

;Especificación Sintáctica (gramática)

(define grammar-simple-interpreter
  '((programa (expresion) un-program)
    (expresion (numero) numero-lit)

    (expresion (texto) texto-lit)
    
    (expresion (identificador) var-exp)
    
    (expresion ("(" expresion primitiva-binaria expresion ")" )
               primapp-bin-exp)

    (expresion (primitiva-unaria "(" expresion ")")
               primapp-un-exp)
    
    (expresion ("si" expresion "entonces" expresion "sino" expresion "finSI")
                condicional-exp)
    
    (expresion ("declarar" "(" (arbno identificador "=" expresion ";") ")" "{" expresion "}")
                variableLocal-exp)
    
    (expresion ("procedimiento" "(" (arbno identificador ",") ")" "haga" expresion "finProc")
                procedimiento-ex)
    
    (expresion ( "evaluar" expresion (arbno expresion) "finEval")
                app-exp)
    
    
    ; características adicionales
    (expresion ("letrec" (arbno identificador "(" (separated-list identificador ",") ")" "=" expresion)  "in" expresion) 
                letrec-exp)
    
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

    (primitiva-binaria ("+") primitiva-suma)
    (primitiva-binaria ("~") primitiva-resta)
    (primitiva-binaria ("/") primitiva-div)
    (primitiva-binaria ("*") primitiva-multi)
    (primitiva-binaria ("concat") primitiva-concat)

    (primitiva-unaria ("longitud") primitiva-longitud)
    (primitiva-unaria ("add1") primitiva-add1)
    (primitiva-unaria ("sub1") primitiva-sub1)))


;Construidos automáticamente: (NO TOCAR)

(sllgen:make-define-datatypes scanner-spec-simple-interpreter grammar-simple-interpreter)

(define show-the-datatypes
  (lambda () (sllgen:list-define-datatypes scanner-spec-simple-interpreter grammar-simple-interpreter)))

;*******************************************************************************************
;Parser, Scanner, Interfaz (NO TOCAR)

;El FrontEnd (Análisis léxico (scanner) y sintáctico (parser) integrados)

(define scan&parse
  (sllgen:make-string-parser scanner-spec-simple-interpreter grammar-simple-interpreter))

;El Analizador Léxico (Scanner)

(define just-scan
  (sllgen:make-string-scanner scanner-spec-simple-interpreter grammar-simple-interpreter))

;El Interpretador (FrontEnd + Evaluación + señal para lectura )

(define interpretador
  (sllgen:make-rep-loop  "--> "
    (lambda (pgm) (eval-program  pgm)) 
    (sllgen:make-stream-parser 
      scanner-spec-simple-interpreter
      grammar-simple-interpreter)))

;*******************************************************************************************
;El Interprete

;eval-program: <programa> -> numero
; función que evalúa un programa teniendo en cuenta un ambiente dado (se inicializa dentro del programa)

(define eval-program
  (lambda (pgm)
    (cases programa pgm
      (un-program (body)
                 (eval-expresion body (init-env))))))

(define init-env
  (lambda ()
    (extend-env
     '(@a @b @c @d @e)
     (list 1 2 3 "hola" "FLP")
     (empty-env))))

; eval-expresion: <expresion> <enviroment> -> numero
; evalua la expresión en el ambiente de entrada
(define eval-expresion
  (lambda (exp env)
    (cases expresion exp
      (numero-lit (datum) datum)

      (texto-lit (tx) tx)

      
      (var-exp (id) (buscar-variable env id))


      (primapp-bin-exp (val1 prim val2)
                   (let (
                         (args (eval-rands (list val1 val2) env)))
                         (apply-primitive prim args)))

      (primapp-un-exp (prim rand)
                  (let (
                         (args (eval-rands (list rand) env)))
                         (apply-primitive-unario prim args)))

 
      (condicional-exp (test-exp true-exp false-exp)
              (if (true-value? (eval-expresion test-exp env))
                  (eval-expresion true-exp env)
                  (eval-expresion false-exp env)))
      (variableLocal-exp (ids rands body)
               (let ((args (eval-rands rands env)))
                 (eval-expresion body
                                  (extend-env ids args env))))
      (procedimiento-ex (ids body)
                (closure ids body env))
      (app-exp (rator rands)
               (let ((proc (eval-expresion rator env))
                     (args (eval-rands rands env)))
                 (if (procval? proc)
                     (apply-procedure proc args)
                     (eopl:error 'eval-expresion
                                 "Attempt to apply non-procedure ~s" proc))))
      (letrec-exp (proc-names idss bodies letrec-body)
                  (eval-expresion letrec-body
                                   (extend-env-recursively proc-names idss bodies env))))))

; funciones auxiliares para aplicar eval-expresion a cada elemento de una 
; lista de operandos (expresiones)
(define eval-rands
  (lambda (rands env)
    (map (lambda (x) (eval-rand x env)) rands)))

(define eval-rand
  (lambda (rand env)
    (eval-expresion rand env)))

;apply-primitive: <primitiva> <list-of-expresion> -> numero
(define apply-primitive
  (lambda (prim args)
    (cases primitiva-binaria prim
      (primitiva-suma () (+ (car args) (cadr args)))
      (primitiva-resta () (- (car args) (cadr args)))
      (primitiva-div () (/ (car args) (cadr args)))
      (primitiva-multi () (* (car args) (cadr args)))
      (primitiva-concat () (string-append (car args) (cadr args)))

      
      )))


(define apply-primitive-unario
  (lambda (prim args)
    (cases primitiva-unaria prim
      (primitiva-longitud () (string-length (car args)))
      (primitiva-add1 () (+ (car args) 1))
      (primitiva-sub1 () (- (car args) 1))
      )))

;true-value?: determina si un valor dado corresponde a un valor booleano falso o verdadero
(define true-value?
  (lambda (x)
    (not (zero? x))))

;*******************************************************************************************
;Procedimientos
(define-datatype procval procval?
  (closure
   (ids (list-of symbol?))
   (body expresion?)
   (env environment?)))

;apply-procedure: evalua el cuerpo de un procedimientos en el ambiente extendido correspondiente
(define apply-procedure
  (lambda (proc args)
    (cases procval proc
      (closure (ids body env)
               (eval-expresion body (extend-env ids args env))))))

;*******************************************************************************************
;Ambientes

;definición del tipo de dato ambiente
(define-datatype environment environment?
  (empty-env-record)
  (extended-env-record (syms (list-of symbol?))
                       (vals (list-of scheme-value?))
                       (env environment?))
  (recursively-extended-env-record (proc-names (list-of symbol?))
                                   (idss (list-of (list-of symbol?)))
                                   (bodies (list-of expresion?))
                                   (env environment?)))

(define scheme-value? (lambda (v) #t))

;empty-env:      -> enviroment
;función que crea un ambiente vacío
(define empty-env  
  (lambda ()
    (empty-env-record)))       ;llamado al constructor de ambiente vacío 


;extend-env: <list-of symbols> <list-of numbers> enviroment -> enviroment
;función que crea un ambiente extendido
(define extend-env
  (lambda (syms vals env)
    (extended-env-record syms vals env)))

;extend-env-recursively: <list-of symbols> <list-of <list-of symbols>> <list-of expresions> environment -> environment
;función que crea un ambiente extendido para procedimientos recursivos
(define extend-env-recursively
  (lambda (proc-names idss bodies old-env)
    (recursively-extended-env-record
     proc-names idss bodies old-env)))


;función que busca un símbolo en un ambiente
(define buscar-variable
  (lambda (env sym)
    (cases environment env
      (empty-env-record ()
                        (eopl:error 'empty-env "Error, la variable ~s ~s"  sym " no existe"))
      (extended-env-record (syms vals old-env)
                           (let ((pos (list-find-position sym syms)))
                             (if (number? pos)
                                 (list-ref vals pos)
                                 (buscar-variable old-env sym))))
      (recursively-extended-env-record (proc-names idss bodies old-env)
                                       (let ((pos (list-find-position sym proc-names)))
                                         (if (number? pos)
                                             (closure (list-ref idss pos)
                                                      (list-ref bodies pos)
                                                      env)
                                             (buscar-variable old-env sym)))))))


;****************************************************************************************
;Funciones Auxiliares

; funciones auxiliares para encontrar la posición de un símbolo
; en la lista de símbolos de unambiente

(define list-find-position
  (lambda (sym los)
    (list-index (lambda (sym1) (eqv? sym1 sym)) los)))

(define list-index
  (lambda (pred ls)
    (cond
      ((null? ls) #f)
      ((pred (car ls)) 0)
      (else (let ((list-index-r (list-index pred (cdr ls))))
              (if (number? list-index-r)
                (+ list-index-r 1)
                #f))))))

;******************************************************************************************
;Pruebas
(interpretador)
