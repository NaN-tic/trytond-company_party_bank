#This file is part company_party_bank module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = [
    'Party',
    ]
__metaclass__ = PoolMeta


class Party:
    __name__ = 'party.party'

    def get_payable_bank_account(self):
        PartyBankAccount = Pool().get('party.bank.account')
        company = Transaction().context.get('company')
        if company:
            accounts = PartyBankAccount.search([
                ('company', '=', company),
                ('party', '=', self.id)
                ], limit=1)
            if accounts:
                return accounts[0].payable_bank_account

    def get_receivable_bank_account(self):
        PartyBankAccount = Pool().get('party.bank.account')
        company = Transaction().context.get('company')
        if company:
            accounts = PartyBankAccount.search([
                ('company', '=', company),
                ('party', '=', self.id)
                ], limit=1)
            if accounts:
                return accounts[0].receivable_bank_account
