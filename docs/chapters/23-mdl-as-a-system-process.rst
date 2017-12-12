Chapter 23. MDL as a System Process
===================================

This chapter treats MDL considered as executing in an operating-system
process, and interactions between MDL and other operating-system
processes. See also section 21.8.13.

23.1. TIME
----------

``TIME`` takes any number of arguments, which are evaluated but ignored,
and returns a ``FLOAT`` giving the number of seconds of CPU time the MDL
process has used so far. ``TIME`` is often used in machine-level
debugging to examine the values of its arguments, by having MDL’s
superior process (say, DDT) plant a breakpoint in the code for ``TIME``.

23.2. Names
-----------

::

    <UNAME>

returns a ``STRING`` which is the “user name” of MDL’s process. This is
the “uname” process-control variable in the ITS version and the
logged-in directory in the Tenex and Tops-20 versions.

::

    <XUNAME>

returns a ``STRING`` which is the “intended user name” of MDL’s process.
This is the “xuname” process-control variable in the ITS version and
identical to ``<UNAME>`` in the Tenex and Tops-20 versions.

::

    <JNAME>

returns a ``STRING`` which is the “job name” of MDL’s process. This is
the “jname” process-control variable in the ITS version and the
``SETNM`` name in the Tenex and Tops-20 versions. The characters belong
to the “sixbit” or “printing” subset of ASCII, namely those between
``<ASCII *40*>`` and ``<ASCII *137*>`` inclusive.

::

    <XJNAME>

returns a ``STRING`` which is the “intended job name” of MDL’s process.
This is the “xjname” process-control variable in the ITS version and
identical to ``<JNAME>`` in the Tenex and Tops-20 versions.

23.3. Exits
-----------

::

    <LOGOUT>

attempts to log out the process in which it is executed. It will succeed
only if the MDL is the top-level process, that is, it is running
disowned or as a daemon. If it succeeds, it of course never returns. If
it does not, it returns ``#FALSE ()``.

::

    <QUIT>

causes MDL to stop running, in an orderly manner. In the ITS version, it
is equivalent to a ``.LOGOUT 1`` instruction. In the Tenex and Tops-20
versions, it is equivalent to a control-C signal, and control passes to
the superior process.

::

    <VALRET string-or-fix>

(“value return”) seldom returns. It passes control back up the process
tree to the superior of MDL, passing its argument as a message to that
superior. If it does return, the value is ``#FALSE ()``. If the argument
is a ``STRING``, it is passed to the superior as a command to be
executed, via ``.VALUE`` in the ITS version and ``RSCAN`` in the Tops-20
version. If the argument is a ``FIX``, it is passed to the superior as
the “effective address” of a ``.BREAK 16``, instruction in the ITS
version and ignored in other versions.

23.4. Inter-process Communication
---------------------------------

All of the ``SUBR``\ s in this section are available only in the ITS
version.

The IPC (“inter-process communication”) device is treated as an I/O
device by ITS but not explicitly so by MDL: that is, it is never
``OPEN``\ ed. It allows MDL to communicate with other ITS processes by
means of sending and receiving messages. A process identifies itself as
sender or recipient of a message with an ordered pair of “sixbit”
``STRING``\ s, which are often but not always ``<UNAME>`` and
``<JNAME>``. A message has a “body” and a “type”.

23.4.1. SEND and SEND-WAIT
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    <SEND othern1 othern2 body type mynamel myname2>

    <SEND-WAIT othern1 othern2 body type mynamel myname2>

both send an IPC message to any job that is listening for it as
*othern1* *othern2*. *body* must be either a ``STRING``, or a
``UVECTOR`` of objects of ``PRIMTYPE`` ``WORD``. *type* is an optional
``FIX``, ``0`` by default, which is part of the information the other
guy receives. The last two arguments are from whom the message is to be
sent. These are optional, and ``<UNAME>`` and ``<JNAME>`` respectively
are used by default. ``SEND`` returns a ``FALSE`` if no one is
listening, while ``SEND-WAIT`` hangs until someone wants it. Both return
``T`` if someone accepts the message.

23.4.2. The “IPC” Interrupt
~~~~~~~~~~~~~~~~~~~~~~~~~~~

When your MDL process receives an IPC message, ``"IPC"`` occurs (chapter
21). A handler is called with either four or six arguments gleaned from
the message. *body*, *type*, *othern1*, and *othern2* are supplied only
if they are not this process’s ``<UNAME>`` and ``<JNAME>``.

There is a built-in ``HANDLER`` for the ``"IPC"`` interrupt, with a
handler named ``IPC-HANDLER`` and ``0`` in the ``PROCESS`` slot. The
handler prints out on the terminal the *body*, whom it is from, the
*type* if not ``0``, and whom it is to if not ``<UNAME>`` ``<JNAME>``.
If the *type* is ``1`` and the *body* is a ``STRING``, then, after the
message information is printed out, the ``STRING`` is ``PARSE``\ d and
``EVAL``\ uated.

23.4.3. IPC-OFF
~~~~~~~~~~~~~~~

``<IPC-OFF>`` stops all listening on the IPC device.

23.4.4. IPC-ON
~~~~~~~~~~~~~~

::

    <IPC-ON myname1 myname2>

causes listening on the IPC device as *myname1* *myname2*. If no
arguments are provided, listening is on ``<UNAME>`` ``<JNAME>``. When a
message arrives, ``"IPC"`` occurs.

MDL is initially listening as ``<UNAME>`` ``<JNAME>`` with the built-in
``HANDLER`` set up on the ``"IPC"`` interrupt with a priority of ``1``.

23.4.5. DEMSIG
~~~~~~~~~~~~~~

::

    <DEMSIG daemon:string>

signals to ITS (directly, not via the IPC device) that the daemon named
by its argument should run now. It returns ``T`` if the daemon exists,
``#FALSE ()`` otherwise.
