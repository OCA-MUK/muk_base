###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK Branding 
#    (see https://mukit.at).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import api, SUPERUSER_ID
from odoo.release import version_info
from odoo.tools import config, convert_file
from odoo.modules.module import get_module_resource

from . import models
from . import tools

#----------------------------------------------------------
# Patch System on Load
#----------------------------------------------------------

def _patch_system():
    from . import patch
    
#----------------------------------------------------------
# Hooks
#----------------------------------------------------------

def _pre_init_debrand_system(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.translation'].clear_caches
    
def _post_init_debrand_system(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for lang in env['res.lang'].search([('active','=',True)]).mapped('code'):
        env['base.language.install'].create({
            'lang': lang,
            'overwrite': True
        }).lang_install()
        env['base.update.translations'].create({
            'lang': lang
        }).act_update()
    env['ir.translation'].clear_caches
    
