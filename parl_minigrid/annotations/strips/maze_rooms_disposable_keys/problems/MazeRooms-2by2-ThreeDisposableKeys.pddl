;;; auto-generated problem instance in parl_minigrid
;;; captital letters for static predicates
;;; R-c-r - room at column c and row r in a room grid
;;; D-color-c1-r1-c2-r2 - door with color linking R-c1-r1 and R-c2-r2 
;;; K-color-i - key with color with numeric index i
;;; (CONNECTED-ROOMS R-0-0 R-0-1) connected room at (0,0) and room at (0,1)
;;; (LINK D-yellow-0-0-0-1 R-0-0 R-0-1) yellow door links rooms at (0,0) and (0,1)
;;; (unlocked D-yellow-0-0-0-1) door D-yellow-0-0-0-1 is unlocked
;;; (KEYMATCH K-yellow-0 D-yellow-0-0-0-1) key k-yellow-0 matches door D-yellow-0-0-0-1
;;; (key-unused k-yellow-0) key k-yellow-0 is not used 
;
;   
;   
(define (problem MazeRooms-2by2-ThreeDisposableKeys)
        (:domain MazeRoomsDisposableKeys)
        (:objects
            R-0-0 R-0-1 R-1-0 R-1-1 -  room
            K-yellow-0 K-yellow-1 K-purple-2 - key
            D-yellow-0-0-0-1 D-purple-1-0-1-1 D-yellow-0-0-1-0 - door
        )
        (:init
			(CONNECTED-ROOMS R-0-0 R-0-1)
			(CONNECTED-ROOMS R-0-0 R-1-0)
			(CONNECTED-ROOMS R-0-1 R-0-0)
			(CONNECTED-ROOMS R-1-0 R-0-0)
			(CONNECTED-ROOMS R-1-0 R-1-1)
			(CONNECTED-ROOMS R-1-1 R-1-0)
			(LINK D-purple-1-0-1-1 R-1-0 R-1-1)
			(LINK D-purple-1-0-1-1 R-1-1 R-1-0)
			(LINK D-yellow-0-0-0-1 R-0-0 R-0-1)
			(LINK D-yellow-0-0-0-1 R-0-1 R-0-0)
			(LINK D-yellow-0-0-1-0 R-0-0 R-1-0)
			(LINK D-yellow-0-0-1-0 R-1-0 R-0-0)
			(KEYMATCH K-purple-2 D-purple-1-0-1-1)
			(KEYMATCH K-yellow-0 D-yellow-0-0-0-1)
			(KEYMATCH K-yellow-0 D-yellow-0-0-1-0)
			(KEYMATCH K-yellow-1 D-yellow-0-0-0-1)
			(KEYMATCH K-yellow-1 D-yellow-0-0-1-0)
			(at-agent R-0-0)
			(at K-purple-2 R-0-1)
			(at K-yellow-0 R-0-0)
			(at K-yellow-1 R-1-0)
			(locked D-purple-1-0-1-1)
			(locked D-yellow-0-0-0-1)
			(locked D-yellow-0-0-1-0)
			(empty-hand)
			(key-unused K-purple-2)
			(key-unused K-yellow-0)
			(key-unused K-yellow-1)
        )
        (:goal 
            (and
			(at-agent R-1-1)
            )
        )
)
