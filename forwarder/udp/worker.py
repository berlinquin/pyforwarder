#
#   pyforwarder a raw socket proxy with optional SSL/TLS termination and trace capability
#   Copyright (C) 2018-2020 Marc Bertens-Nguyen m.bertens@pe2mbs.nl
#
#   This library is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Library General Public License GPL-2.0-only
#   as published by the Free Software Foundation; either version 2 of the
#   License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#   Library General Public License for more details.
#
#   You should have received a copy of the GNU Library General Public
#   License GPL-2.0-only along with this library; if not, write to the
#   Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301 USA
#
import traceback
import time
import select
import forwarder.api as API


def udpWorker( listeners ):
    inputs = [ ]
    for listener in listeners:
        inputs.append( listener )

    outputs = [ ]
    excepts = inputs
    try:
        while inputs and API.running:
            readable, writable, exceptional = select.select( inputs, outputs, excepts )
            for rd in readable:
                rd.transfer( 4096 )

            for ex in exceptional:
                inputs.remove( ex )

        time.sleep( 1 )

    except KeyboardInterrupt:
        API.running = False

    except Exception:
        API.logger.error( traceback.format_exc() )

    finally:
        API.logger.info( "shudown the listeners" )
        for sock in listeners:
            sock.close()

    return