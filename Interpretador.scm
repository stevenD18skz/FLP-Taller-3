#lang eopl


;******************************************************************************************
;;;                                                                                       *
;;Brayan Steven Narvaez Valdes - 2226675-3743                                             *
;;Miguel Alejandro Tami Lobo - 2228409                                                    *
;;;                                                                                       *
;******************************************************************************************




;******************************************************************************************
;;;;; Interpretador para lenguaje con condicionales, ligadura local, procedimientos y 
;;;;; procedimientos recursivos
;;
;; La definición BNF para las expresiones del lenguaje:
;;
;;  <programa>      ::= <expresion>
;;                      <un-programa (exp)>
;;
;;  <expresion>     ::= <numero>
;;                      numero-lit (num)
;;                  ::= "\""<texto>"\""
;;                      texto-lit(txt)
;;                  ::= <identificador>
;;                      var-exp (id)
;;                  ::= (<expresion> <primitiva-binaria> <expresion>)
;;                      primapp-bin-exp (exp1 prim-binaria exp2)
;;                  ::= <primitiva-unaria> (<expresion>})
;;                      primapp-un-exp (prim-unaria exp)
;;                  ::= Si <expresion> entonces <expresion> sino <expresion> finSi
;;                      condicional-exp (test-exp true-exp false-exp)
;;                  ::= declarar (<identificador> = <expresion> (;)) { <expresion> }
;;                      variableLocal-exp (ids exps cuerpo)
;;                  ::=  procedimiento (<identificador>*',') haga <expresion> finProc
;;                      procedimiento-exp (ids cuerpo)
;;                  ::= "evaluar" expresion (expresion ",")* finEval
;;                      app-exp(exp exps)
;;                  ::= funRecursiva:  {<identificador> ({<identificador>}*(,)) = <expresion>(;)}* {<expresion>}
;;                      rec-exp (proc-names idss bodies bodyrec)
;;
;;  <primitiva-binaria>   ::= | + | ~  | / | * | concat |
;;  <primitiva-unaria>    ::= | longitud | add1 | sub1 |

;******************************************************************************************

;******************************************************************************************
;Especificación Léxica

(define scanner-spec-simple-interpreter
  '((white-sp
     (whitespace) skip)

    (comment
     ("%" (arbno (not #\newline))) skip)

    (identificador
     ("@" letter (arbno (or letter digit "?"))) symbol)
  
    (numero
     (digit (arbno digit)) number)
    (numero
     (digit (arbno digit) "." digit (arbno digit)) number)
    (numero
     ("-" digit (arbno digit) "." digit (arbno digit)) number)
    (numero
     ("-" digit (arbno digit)) number)
  
    (texto
     ((or letter "-") (arbno (or letter digit "-" ":"))) string)
  ))

;Especificación Sintáctica (gramática)

(define grammar-simple-interpreter
  '((programa (expresion)
                un-program)
    
    (expresion (numero)
                numero-lit)

    (expresion ("\""texto"\"")
                texto-lit)
    
    (expresion (identificador)
                var-exp)
    
    (expresion ("(" expresion primitiva-binaria expresion ")")
                primapp-bin-exp)

    (expresion (primitiva-unaria "(" expresion ")")
                primapp-un-exp)
    
    (expresion ("Si" expresion "entonces" expresion "sino" expresion "finSI")
                condicional-exp)
    
    (expresion ("declarar" "(" (separated-list identificador "=" expresion ";") ")" "{" expresion "}")
                variableLocal-exp)
    
    (expresion ("procedimiento" "(" (separated-list identificador ",") ")" "haga" expresion "finProc")
                procedimiento-exp)
    
    (expresion ( "evaluar" expresion "(" (separated-list expresion ",") ")" "finEval")
                app-exp)

    (expresion ("funRecursiva:" (arbno identificador "(" (separated-list identificador ",") ")" "=" expresion ";")  "{" expresion "}")
                rec-exp)
    
    ;

    (primitiva-binaria ("+") primitiva-suma)
    (primitiva-binaria ("~") primitiva-resta)
    (primitiva-binaria ("/") primitiva-div)
    (primitiva-binaria ("*") primitiva-multi)
    (primitiva-binaria ("concat") primitiva-concat)

    
    (primitiva-unaria ("add1") primitiva-add1)
    (primitiva-unaria ("sub1") primitiva-sub1)
    (primitiva-unaria ("longitud") primitiva-longitud)
    ))
;


;Construidos automáticamente:
(sllgen:make-define-datatypes scanner-spec-simple-interpreter grammar-simple-interpreter)

(define show-the-datatypes
  (lambda () (sllgen:list-define-datatypes scanner-spec-simple-interpreter grammar-simple-interpreter)))





;*******************************************************************************************
;Parser, Scanner, Interfaz

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
      (empty-env)
     )))

; eval-expresion: <expresion> <enviroment> -> numero
; evalua la expresión en el ambiente de entrada
(define eval-expresion
  (lambda (exp env)
    (cases expresion exp
      
      (numero-lit (int) int)

      (texto-lit (str) str)
      
      (var-exp (id) (buscar-variable env id))
      
      (primapp-bin-exp (exp1 prim-binaria exp2)
                   (let (
                         (args (eval-rands (list exp1 exp2) env))
                         )
                         (apply-primitive-bin prim-binaria args)
                     ))

      (primapp-un-exp (prim-unaria exp)
                  (let (
                        (args (eval-rand exp env))
                         )
                         (apply-primitive-un prim-unaria args)
                    ))

      (condicional-exp (test-exp true-exp false-exp)
                       (if (valor-verdadero? (eval-expresion test-exp env))
                           (eval-expresion true-exp env)
                           (eval-expresion false-exp env)))

      (variableLocal-exp (ids rands body)
                         (let (
                               (args (eval-rands rands env))
                               )
                           (eval-expresion body (extend-env ids args env))
                           ))
      
      (procedimiento-exp (ids body)
                (cerradura ids body env))

      (app-exp (rator rands)
               (let (
                     (proc (eval-expresion rator env))
                     (args (eval-rands rands env))
                     )
                 (if (procval? proc)
                     (apply-procedure proc args)
                     (eopl:error 'eval-expresion "estas tratando de ejecutar algo que no es un procedimiento ~s" proc)
                     )
                 ))
      
      (rec-exp (proc-names idss bodies letrec-body)
                  (eval-expresion letrec-body (extend-env-recursively proc-names idss bodies env)))
      )))

; funciones auxiliares para aplicar eval-expresion a cada elemento de una 
; lista de operandos (expresiones)
(define eval-rands
  (lambda (rands env)
    (map (lambda (x) (eval-rand x env)) rands)))

(define eval-rand
  (lambda (rand env)
    (eval-expresion rand env)))

;apply-primitive-bin: <primitiva-binaria> <lista-de-expresiones> -> numero
(define apply-primitive-bin
  (lambda (prim args)
    (cases primitiva-binaria prim
      (primitiva-suma   () (+ (car args) (cadr args)))
      (primitiva-resta  () (- (car args) (cadr args)))
      (primitiva-div    () (/ (car args) (cadr args)))
      (primitiva-multi  () (* (car args) (cadr args)))
      (primitiva-concat () (string-append (car args) (cadr args)))
      )))


;apply-primitive-un: <primitiva-unaria> <lista-de-expresiones> -> numero
(define apply-primitive-un
  (lambda (prim args)
    (cases primitiva-unaria prim
      (primitiva-add1     () (+ args 1))
      (primitiva-sub1     () (- args 1))
      (primitiva-longitud () (string-length args))
      )))

;valor-verdadero?: determina si un valor dado corresponde a un valor booleano falso o verdadero
(define valor-verdadero?
  (lambda (x)
    (not (zero? x))))

;*******************************************************************************************
;Procedimientos
(define-datatype procval procval?
  (cerradura
   (ids (list-of symbol?))
   (body expresion?)
   (env environment?)))

;apply-procedure: evalua el cuerpo de un procedimientos en el ambiente extendido correspondiente
(define apply-procedure
  (lambda (proc args)
    (cases procval proc
      (cerradura (ids body env)
               (eval-expresion body (extend-env ids args env))))))

;*******************************************************************************************
;Ambientes

;definición del tipo de dato ambiente
(define-datatype environment environment?
  (empty-env-record)
  (extended-env-record (syms (list-of symbol?))
                       (vals (list-of scheme-value?))
                       (env environment?)
                       )
  (recursively-extended-env-record (proc-names (list-of symbol?))
                                   (idss (list-of (list-of symbol?)))
                                   (bodies (list-of expresion?))
                                   (env environment?)
                                   )
  )

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
                                             (cerradura (list-ref idss pos)
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


;a✓✓✓
;b✓✓✓
;c✓✓✓
;d✓✓ (falta tomar una meleccion en multiplicar)
;e
;f
;////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
;                         ==================>  SOLUCIONES DE PUNTOS   <==================
;////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



;************************************************************************************************************************
;---------------------------------------------------> PUNTO A <----------------------------------------------------------
;************************************************************************************************************************
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                                        ;
;  areaCirculo (numero -> numero):                                                      ;
;                                                                                       ;
;  Proposito:                                                                           ;
;    @r -> a: recibiendo el radio de un ciruclo, calcula la area de este                ;
;                                                                                       ;
;  Args:                                                                                ;
;    @r: El número entero que representa el readio del ciruclo                          ; 
;                                                                                       ;
;  Returns:                                                                             ;
;    a: el valor del area del ciruclo                                                   ;
;                                                                                        ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; declarar (
;   @radio=2.5;
;   @areaCirculo=procedimiento(@r) haga 
;     declarar (
;       @pi=3.1416
;     )
;     {
;       (@pi*(@r*@r))
;      } finProc
;   ) {
;     evaluar @areaCirculo(@radio) finEval
;    }







;************************************************************************************************************************
;---------------------------------------------------> PUNTO B <----------------------------------------------------------
;************************************************************************************************************************
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                                        ;
;; factorial (numero -> numero):                                                        ;
;                                                                                       ;
;  Proposito:                                                                           ;
;    @n -> N ; Calcula el factorial de un número usando recursividad.                   ;
;                                                                                       ;
;  Args:                                                                                ;
;    @n: El número entero no negativo del que se quiere calcular el factorial.          ;
;                                                                                       ;
;  Returns:                                                                             ;
;    El valor del factorial de @n                                                       ;
;                                                                                        ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; funRecursiva:
;   @factorial(@n)=Si @n
;                         entonces (@n * evaluar  @factorial(sub1(@n)) finEval)
;                         sino 1
;                     finSI;
;   { evaluar @factorial(5) finEval }



; funRecursiva:
;   @factorial(@n)=Si @n
;                       entonces (@n * evaluar  @factorial(sub1(@n)) finEval)
;                       sino 1
;                     finSI;
;   {
;    declarar (
;     @valor = 10
;    ) {
;       evaluar @factorial(@valor) finEval
;      }
;    }




;************************************************************************************************************************
;---------------------------------------------------> PUNTO C <----------------------------------------------------------
;************************************************************************************************************************
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                                        ;
;; sumar (numero * numero -> numero):                                                   ;
;                                                                                       ;
;  Proposito:;                                                                          ;
;   @a x @b -> N ; Función recursiva que suma dos números enteros.                      ;
;                                                                                       ;
;  Args:                                                                                ;
;    @a: El primer número entero a sumar.                                               ;
;    @b: El segundo número entero a sumar.                                              ;
;                                                                                       ;                                                                                      ;
;  Returns:;                                                                            ;
;    La suma de a y b                                                                   ;
;                                                                                        ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; funRecursiva:
;   @sumar(@a, @b) = Si @a
;                       entonces  add1(evaluar @sumar(sub1(@a),@b) finEval)
;                       sino @b
;                     finSI;
;   { evaluar @sumar(4, 5) finEval }
                                                                                                                                                                                             





;************************************************************************************************************************
;---------------------------------------------------> PUNTO D <----------------------------------------------------------
;************************************************************************************************************************
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                                                ;
;; resta:                                                                                        ;
;                                                                                                ;
;  Proposito:                                                                                    ;
;    @a x @b -> N ; Resta dos números enteros de forma recursiva, haciendo uso de add1 y sub1    ;
;                                                                                                ;
;  Args:                                                                                         ;
;    @a: El primer número entero.                                                                ;
;    @b: El segundo número entero.                                                               ;
;                                                                                                ;
;  Returns:                                                                                      ;
;    La diferencia entre @x e @y                                                                 ;
;                                                                                                ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; funRecursiva:
;   @restar(@a, @b) = Si @b
;                         entonces evaluar @restar(sub1(@a) , sub1(@b)) finEval
;                         sino @a
;                       finSI ;
;   { evaluar @restar(10, 3) finEval }




;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                                        ;
;; multiplicar:                                                                          ; 
;  Proposito:                                                                            ;
;   @x x @y -> N ; Multiplica dos números enteros                                        ;
;                                                                                        ;
;  Args:                                                                                 ;
;    @x: El primer número entero                                                         ;
;    @y: El segundo número entero                                                        ;
;                                                                                        ;
;  Returns:                                                                              ;
;    El producto de @x e @y                                                              ;
;                                                                                        ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; funRecursiva:
;   @sumar(@a, @b) = Si @a
;                       entonces evaluar @sumar (sub1(@a),add1(@b)) finEval
;                       sino @b
;                     finSI;
; 
;   @multiplicar(@x, @y) = Si @y
;                             entonces evaluar @sumar (@x, evaluar @multiplicar (@x,sub1(@y)) finEval) finEval
;                             sino 0
;                           finSI;
; 
;   { evaluar @multiplicar (10,3) finEval }





;************************************************************************************************************************
;---------------------------------------------------> PUNTO E <----------------------------------------------------------
;************************************************************************************************************************
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                                        ;
;; integrantes (() -> texto):                                                            ; 
;  Proposito:                                                                            ;
;   () -> S ; Retorna una cadena de texto con los nombres de los integrantes             ;
;                                                                                        ;
;  Args:                                                                                 ;
;    ()                                                                                  ;
;                                                                                        ;
;  Returns:                                                                              ;
;    Un string de los nombres de los integrantes                                         ;
;                                                                                        ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                                        ;
;; saludar (procedimietno -> procedimiento):                                             ; 
;  Proposito:                                                                            ;
;   F -> S ; Devolver una funcion para el decorador                                      ;
;                                                                                        ;
;  Args:                                                                                 ;
;    @funcion: funcion que se evalua                                                     ;
;                                                                                        ;
;  Returns:                                                                              ;
;    Un procedimiento que concatena "Hola:" con la evaluacion del procedimiento          ;
;    que se paso como parametro                                                          ;
;                                                                                        ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


; declarar(
;   @integrantes  = procedimiento () haga
;                                 "Steven-Miguel"
;                   finProc;
;   @saludar      = procedimiento (@funcion) haga
;                                 procedimiento () haga
;                                               ("Hola:" concat evaluar @funcion () finEval)
;                                 finProc
;                   finProc                
;   ) {
;   declarar (
;     @decorate  = evaluar @saludar(@integrantes) finEval
;     ) {
;     evaluar @decorate()  finEval
;     }
;   }









;************************************************************************************************************************
;---------------------------------------------------> PUNTO F <----------------------------------------------------------
;************************************************************************************************************************
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                                        ;
;; integrantes (() -> texto):                                                            ; 
;  Proposito:                                                                            ;
;   () -> S ; Retorna una cadena de texto con los nombres de los integrantes             ;
;                                                                                        ;
;  Args:                                                                                 ;
;    ()                                                                                  ;
;                                                                                        ;
;  Returns:                                                                              ;
;    Un string de los nombres de los integrantes                                         ;
;                                                                                        ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                                        ;
;; saludar (procedimietno -> procedimiento):                                             ; 
;  Proposito:                                                                            ;
;   F -> S ; Devolver una funcion para el decorador                                      ;
;                                                                                        ;
;  Args:                                                                                 ;
;    @funcion: funcion que se evalua                                                     ;
;                                                                                        ;
;  Returns:                                                                              ;
;    Un procedimiento que concatena "Hola:" con la evaluacion del procedimiento          ;
;    que se paso como parametro                                                          ;
;                                                                                        ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                                        ;
;; decorate (texto -> texto):                                                            ; 
;  Proposito:                                                                            ;
;   S -> S' ; concatenar un mensaje personalizado con la evaluacion de saludar           ;
;                                                                                        ;
;  Args:                                                                                 ;
;    @final: string que representa el mensaje personalizado                              ;
;                                                                                        ;
;  Returns:                                                                              ;
;    Un string con la concatenacion del mensaje junto con el restulado de @saludar       ;
;                                                                                        ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; declarar(
;   @integrantes  = procedimiento () haga "Steven-Miguel" finProc;
;   @saludar      = procedimiento (@funcion) haga
;                                 procedimiento () haga
;                                               ("Hola:" concat evaluar @funcion () finEval)
;                                 finProc
;                   finProc               
;   ) {
;   declarar (
;     @decorate   = procedimiento (@final) haga
;                                 (evaluar evaluar @saludar(@integrantes) finEval () finEval concat @final)
;                   finProc
;     ) {
;     evaluar @decorate("-ProfesoresFLP")  finEval
;     }
;   }











;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;                                                                                        ;
;; saludar (procedimietno -> procedimiento):                                             ; 
;  Proposito:                                                                            ;
;   F -> S ; Devolver una funcion para el decorador                                      ;
;                                                                                        ;
;  Args:                                                                                 ;
;    @funcion: funcion que se evalua                                                     ;
;                                                                                        ;
;  Returns:                                                                              ;
;    Un procedimiento que recibe a su vez un parametro adicional con                     ;
;    el mensaje personalizado y devuelve el todas las concatenaciones                    ;
;                                                                                        ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; declarar(
;   @integrantes  = procedimiento () haga "Steven-Miguel" finProc;
;   @saludar      = procedimiento (@funcion) haga
;                                 procedimiento (@adios) haga
;                                               (("hola:" concat evaluar @funcion () finEval) concat @adios)
;                                 finProc
;                   finProc                
;   ) {
;   declarar (
;     @decorate  = evaluar @saludar(@integrantes) finEval
;     ) {
;     evaluar @decorate("-ProfesoresFLP")  finEval
;     }
;   }







;INICIAR EL INTERPRETADOR
(interpretador)
