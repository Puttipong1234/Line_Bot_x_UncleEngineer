========
Email To
========


.. image:: https://img.shields.io/pypi/v/email_to.svg
        :target: https://pypi.python.org/pypi/email_to

.. image:: https://img.shields.io/travis/abkfenris/email_to.svg
        :target: https://travis-ci.org/abkfenris/email_to

.. image:: https://readthedocs.org/projects/email-to/badge/?version=latest
        :target: https://email-to.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/abkfenris/email_to/shield.svg
     :target: https://pyup.io/repos/github/abkfenris/email_to/
     :alt: Updates


Simplyify sending HTML emails


* Free software: MIT license
* Documentation: https://email-to.readthedocs.io.

Judgement rendered by:

.. image:: https://api.codacy.com/project/badge/Grade/7dddc6b7000349958d485080f3dda7c1    
        :target: https://www.codacy.com/app/abk/email_to?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=abkfenris/email_to&amp;utm_campaign=Badge_Grade
        :alt: Codacy

.. image:: https://landscape.io/github/abkfenris/email_to/master/landscape.svg?style=flat
   :target: https://landscape.io/github/abkfenris/email_to/master
   :alt: Code Health

.. image:: https://codeclimate.com/github/abkfenris/email_to/badges/gpa.svg
   :target: https://codeclimate.com/github/abkfenris/email_to
   :alt: Code Climate

.. image:: https://scrutinizer-ci.com/g/abkfenris/email_to/badges/quality-score.png?b=master
        :target: https://scrutinizer-ci.com/g/abkfenris/email_to/
        :alt: scrutinizer

Features
--------

The built in Python modules for sending email are powerful, but require a lot of
boilerplate to write an HTML formatted email.

.. code-block:: python

        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        import smtplib

        message = MIMEMultipart('alternative')
        message['Subject'] = 'Test'
        message['From'] = 'user@gmail.com'
        message['To'] = 'someone@else.com'

        message.attach(MIMEText('# A Heading\nSomething else in the body', 'plain')
        message.attach(MIMEText('<h1 style="color: blue">A Heading</a><p>Something else in the body</p>', 'html')

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('user@gmail.com', 'password')
        server.sendmail('user@gmail.com', 'someone@else.com', message.as_string())
        server.quit()

With ``email_to`` sending a simple email becomes much more succint.

.. code-block:: python

        import email_to

        server = email_to.EmailServer('smtp.gmail.com', 587, 'user@gmail.com', 'password')
        server.quick_email('someone@else.com', 'Test',
                           ['# A Heading', 'Something else in the body'],
                           style='h1 {color: blue}')


``email_to`` also supports building a message up, line by line. This is
especially useful for monitoring scripts where there may be several different
conditions of interest.

.. code-block:: python

        import email_to

        server = email_to.EmailServer('smtp.gmail.com', 587, 'user@gmail.com', 'password')

        message = server.message()
        message.add('# Oh boy, something went wrong!')
        message.add('- The server had a hiccup')
        message.add('- The power went out')
        message.add('- Blame it on a rogue backhoe')
        message.style = 'h1 { color: red}'

        message.send('someone@else.com', 'Things did not occur as expected')

Additionally if the server details are not known at the beginning of the message,
that can be handled easily too.

.. code-block:: python

        import email_to

        message = email_to.Message('# Every thing is ok')
        message.add('Everything has been running fine for days.')
        message.add('Probably time to build something new and break everything')
        message.style = 'h1 { color: green }'

        server = email_to.EmailServer('smtp.gmail.com', 587, 'user@gmail.com', 'password')
        server.send_message(message, 'someone@else.com', 'Things are awesome')

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



=======
History
=======

0.1.0 (2017-09-27)
------------------

* First release on PyPI.


