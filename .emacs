
; python stufff
; use spaces instead of tabs.
(setq-default indent-tabs-mode nil);
(setq-default tab-width 4)

;(add-to-list 'load-path "~/.emacs.d/test.el")
;(add-to-list 'auto-mode-alist '("\\.haml\\'" . haml-mode))
;(autoload 'haml-mode "~/.emacs.d/haml-mode.el" nil t)


; SoccerStats.us keybindings
; these are for formatting soccer data text, primarily taken from rsssf

; ‘M-x apply-macro-to-region-lines’
; ‘M-x name-last-kbd-macro’ – Name the last-defined keyboard macro.
; ‘M-x insert-kbd-macro’ – Insert a named keyboard macro at point.


(fset 'remove-duplicate-space "\C-s  \C-b\C-?\C-a")
(fset 'comment-out "*\C-e\C-f")

(fset 'format-round "\C-[xreplace-string\C-mRound\C-mRound:\C-m")

(fset 'format-rsssf-game "\C-s-\C-a; \C-s-\C-b\C-r \C-b\C-f;\C-s \C-s\C-b;\C-a\C-n")
(fset 'format-rsssf-colon-game "\C-s:\C-a; \C-s:\C-b-\C-d\C-r \C-b\C-f;\C-s \C-s\C-b;\C-a\C-n")

(fset 'format-rsssf-game-goals "\C-cg\C-a\C-b\C-b\C-b\C-s[\C-b\C-d\C-s]\C-b\C-d\C-m")

(fset 'format-mexico-goals
   "\C-[\C-s [0-9] \C-b\C-b\C-b;\C-f\C-f-\C-[\C-s [0-9]\C-b\C-k\C-r-\C-f\C-y;\C-a; \C-s[\C-b\C-d\C-s]\C-b\C-d\C-m\C-m")


(fset 'format-double-semicolon "\C-s;;\C-b\C-d\C-s-\C-s\C-f\C-b\C-s \C-b;\C-a\C-n")

(fset 'format-attendance "\C-[\C-s[0-9],[0-9][0-9][0-9]\C-b\C-b\C-b\C-?\C-b\C-b\C-b;")

(fset 'format-penalty "\C-[\C-s[0-9]pen\C-b\C-d\C-?\C-?\C-r \C-f(pk) ")

(fset 'format-penaltyb "\C-s pen\C-b\C-d\C-?\C-?\C-?\C-r \C-f(pk) ")

(fset 'format-own-goal "\C-[\C-s[0-9]og\C-b\C-d\C-?\C-r \C-f(og) ")

(fset 'format-duplicate-scorer "\C-[\C-s [0-9]\C-b\C-w\C-y\C-s,\C-f\C-y")



(defun dates-split
  () 
  (interactive)
  (setq lines 370)
  (setq year 2015)
  (setq year1 (+ 1 year))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Jul \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 7/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Aug \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 8/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Sep \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 9/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Oct \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 10/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Nov \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 11/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Dec \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 12/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Jan \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 1/\C-s]\C-b/" (number-to-string year1) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Feb \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 2/\C-s]\C-b/" (number-to-string year1) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Mar \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 3/\C-s]\C-b/" (number-to-string year1) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Apr \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 4/\C-s]\C-b/" (number-to-string year1) "\C-d\C-m"))
    (error nil))

    (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[May \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 5/\C-s]\C-b/" (number-to-string year1) "\C-d\C-m"))
    (error nil))


  ;(execute-kbd-macro (concat "\C-s[Jul \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 7/\C-s]\C-b/" year "\C-d\C-m"))
)


(defun dates-full
  () 
  (interactive)
  (setq lines 500)
  (setq year 2015)

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Jan \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 1/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Feb \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 2/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Mar \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 3/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Apr \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 4/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[May \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 5/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Jun \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 6/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Jul \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 7/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Aug \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 8/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Sep \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 9/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Oct \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 10/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Nov \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 11/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))

  (condition-case nil
      (apply-macro-to-region-lines 1 lines (concat "\C-s[Dec \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 12/\C-s]\C-b/" (number-to-string year) "\C-d\C-m"))
    (error nil))


  ;(execute-kbd-macro (concat "\C-s[Jul \C-b\C-d\C-?\C-?\C-?\C-?\C-mDate: 7/\C-s]\C-b/" year "\C-d\C-m"))
)



; key bindings

(global-set-key (kbd "C-c c") 'comment-out)

(global-set-key (kbd "C-c a") 'format-attendance)
(global-set-key (kbd "C-c r") 'format-round)

(global-set-key (kbd "C-c m") 'format-mexico-goals)
(global-set-key (kbd "C-c g") 'format-rsssf-game)
(global-set-key (kbd "C-c o") 'format-rsssf-colon-game)
(global-set-key (kbd "C-c ]") 'format-rsssf-game-goals)

(global-set-key (kbd "C-c ;") 'format-double-semicolon)

(global-set-key (kbd "C-c u") 'format-duplicate-scorer)
(global-set-key (kbd "C-c p") 'format-penalty)
(global-set-key (kbd "C-c b") 'format-penaltyb)
(global-set-key (kbd "C-c o") 'format-own-goal)
