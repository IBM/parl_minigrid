(define (domain MazeRooms)
  (:requirements :strips :typing)
    (:types
        room - object
        key - object
        door - object
    )
    (:predicates
        (at-agent ?r - room)

        (at ?k - key ?r - room)

        (carry ?k - key)

        (empty-hand)

        (KEYMATCH ?k - key ?d - door)

        (LINK ?d - door ?r1 - room ?r2 - room)

        (locked ?d - door)

        (unlocked ?d - door)

        (CONNECTED-ROOMS ?r1 - room ?r2 - room)
    )


    ;;; rooms are always connected through a door
    ;;; [r1 - [d] - r2]
    ;;; minigrid env return the location of the room from a grid coordinate
    ;;; d is in r2. this is the same for vertical layout.
    ;;; move-room(d, r1, r2) stops when agent can stand on the d
    ;;; move-room(d, r2, r1) stops when agent passes the door and stand on the grid next to the d
    (:action move-room
        :parameters (?d - door ?r1 - room ?r2 - room)
        :precondition (and
            (CONNECTED-ROOMS ?r1 ?r2)
            (at-agent ?r1)
            (LINK ?d ?r1 ?r2)
            (unlocked ?d)
        )
        :effect (and
            (not (at-agent ?r1))
            (at-agent ?r2)
        )
    )

    ;;; pickup/drop
    (:action pickup
        :parameters (?k - key ?r - room)
        :precondition (and
            (at ?k ?r)
            (at-agent ?r)
            (empty-hand)
        )
        :effect (and
            (not (at ?k ?r))
            (not (empty-hand))
            (carry ?k)
        )
    )

    (:action drop
        :parameters (?k - key ?r - room)
        :precondition (and
            (carry ?k)
            (at-agent ?r)
        )
        :effect (and
            (at ?k ?r)
            (empty-hand)
            (not (carry ?k))
        )
    )

    ;;; lock/unlock
    ;;; unlock the door while standing in r1
    ;;; the door connects to r2
    ;;; [r1 - [d] - r2]
    (:action unlock
        :parameters (?k - key ?d - door ?r1 - room ?r2 - room)
        :precondition (and
            (CONNECTED-ROOMS ?r1 ?r2)
            (at-agent ?r1)
            (LINK ?d ?r1 ?r2)
            (carry ?k)
            (locked ?d)
            (KEYMATCH ?k ?d)
        )
        :effect (and
            (not (locked ?d))
            (unlocked ?d)
        )
    )
)
