
Supported Mailbox Types
=======================

Django Mailbox supports polling both common internet mailboxes like
POP3 and IMAP as well as local file-based mailboxes.

.. table:: 'Protocol' Options

  ============ ============== ===============================================================
  Mailbox Type 'Protocol'://  Notes
  ============ ============== ===============================================================
  POP3         ``pop3://``    Can also specify SSL with ``pop3+ssl://``
  IMAP         ``imap://``    Can also specify SSL and archive with ``imap+ssl://?myarchive``
  Maildir      ``maildir://``
  Mbox         ``mbox://``
  Babyl        ``babyl://``
  MH           ``mh://``
  MMDF         ``mmdf://``
  Piped Mail   *empty*        See :ref:`receiving-mail-from-exim4-or-postfix`
  ============ ============== ===============================================================

.. warning::

   This will delete or move any messages it can find in the inbox you specify;
   do not use an e-mail inbox that you would like to share between
   applications. For the IMAP protocol you can specify an archive folder where
   emails are moved to.


POP3 and IMAP Mailboxes
-----------------------

Mailbox URIs are in the normal URI format::

    protocol://username:password@domain

Basic IMAP Example: ``imap://username:password@server``

Basic POP3 Example: ``pop3://username:password@server``

Most mailboxes these days are SSL-enabled; 
if yours is, add ``+ssl`` to your URI.  
Also, if your username or password include any non-ascii characters,
they should be URL-encoded  (for example, if your username includes an
``@``, it should be changed to ``%40`` in your URI).

If you are using an IMAP Mailbox, you can archive all messages before they
are deleted from the inbox. To archive emails, add the archive folder
name as a queryparemeter to the uri (for example, if your mailbox has a
folder called myarchive, add ``?myarchive`` to the uri).

If you have an account named ``youremailaddress@gmail.com`` with a password
of ``1234`` on GMail, which uses a IMAP server of 'imap.gmail.com', requires
SSL and you want to archive all emails, you would enter the following as 
your URI::

    pop3+ssl://youremailaddress%40gmail.com:1234@pop.gmail.com?[GMAIL]/All Mail


Local File-based Mailboxes
--------------------------

If you happen to want to consume a file-based mailbox like an Maildir, Mbox,
Babyl, MH, or MMDF mailbox, you can use this too by entering the appropriate
'protocol' in the URI.  If you had a maildir, for example, at ``/var/mail/``,
you would enter a URI like::

    maildir:///var/mail

Note that there is an additional ``/`` in the above URI after the protocol; 
this is important.

