#!/usr/bin/env python
#This file is part company_party_bank module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.

import sys
import os
DIR = os.path.abspath(os.path.normpath(os.path.join(__file__,
    '..', '..', '..', '..', '..', 'trytond')))
if os.path.isdir(DIR):
    sys.path.insert(0, os.path.dirname(DIR))

import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import POOL, DB_NAME, USER, CONTEXT, test_view,\
    test_depends
from trytond.transaction import Transaction


class BlankTestCase(unittest.TestCase):
    '''
    Test Blank module.
    '''

    def setUp(self):
        trytond.tests.test_tryton.install_module('company_party_bank')
        self.party = POOL.get('party.party')
        self.baccount = POOL.get('bank.account')

    def test0005views(self):
        '''
        Test views.
        '''
        test_view('company_party_bank')

    def test0006depends(self):
        '''
        Test depends.
        '''
        test_depends()

    def test0040bank_account(self):
        '''
        Default payment bank account.
        '''
        with Transaction().start(DB_NAME, USER, context=CONTEXT) as transaction:
            party, = self.party.search([
                ('name', '=', 'Zikzakmedia'),
                ], limit=1)
            baccount1, = self.baccount.search([
                ('code', '=', '1234567890'),
                ], limit=1)
            baccount2, = self.baccount.search([
                ('code', '=', '0987654321'),
                ], limit=1)
            self.baccount.write([baccount1], {
                    'payable_bank_account': True,
                    'receivable_bank_account': True,
                    })
            self.baccount.write([baccount2], {
                    'payable_bank_account': True,
                    'receivable_bank_account': True,
                    })

def suite():
    suite = trytond.tests.test_tryton.suite()
    from trytond.modules.company.tests import test_company
    for test in test_company.suite():
        if test not in suite:
            suite.addTest(test)
    from trytond.modules.party_bank.tests import test_party_bank
    for test in test_party_bank.suite():
        if test not in suite:
            suite.addTest(test)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        BlankTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
