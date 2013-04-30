#This file is part company_party_bank module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = [
    'BankAccount',
    'PartyBankAccount',
    ]
__metaclass__ = PoolMeta


class BankAccount:
    'Bank Account'
    __name__ = 'bank.account'
    payable_bank_account = fields.Function(fields.Boolean(
        'Default payable bank account',
        help="Check this box if this is the default bank account for "
            "receivable."),
        'get_bank_account', setter='set_bank_accounts')
    receivable_bank_account = fields.Function(fields.Boolean(
        'Default receivable bank account',
        help="Check this box if this is the default bank account for "
            "payments."),
        'get_bank_account', setter='set_bank_accounts')

    def get_bank_account(self, name):
        PartyBankAccount = Pool().get('party.bank.account')
        company = Transaction().context.get('company')
        if company:
            party = self.party.id
            accounts = PartyBankAccount.search([
                ('company', '=', company),
                ('party', '=', party)
                ], limit=1)
            if accounts:
                account, = accounts
                account_bank = getattr(account, name)
                return self == account_bank

    @classmethod
    def set_bank_accounts(cls, bank_accounts, name, value):
        PartyBankAccount = Pool().get('party.bank.account')
        company = Transaction().context.get('company')
        vlist = []
        for bank_account in bank_accounts:
            if not company:
                break
            party = bank_account.party.id
            accounts = PartyBankAccount.search([
                ('company', '=', company),
                ('party', '=', party)
                ], limit=1)
            if not accounts:
                vlist.append({
                        'company': company,
                        'party': party,
                        name: value and bank_account.id or None,
                        })
                continue
            account = accounts[0]
            default_account = getattr(account, name)
            if (default_account == bank_account and \
                    bool(default_account) != value) or \
                    (default_account != bank_account and value):
                PartyBankAccount.write([account], {
                        name: value and bank_account.id or None,
                        })
        if vlist:
            PartyBankAccount.create(vlist)


class PartyBankAccount(ModelSQL, ModelView):
    'Party Bank Account'
    __name__ = 'party.bank.account'
    _rec_name = 'party'
    party = fields.Many2One('party.party', 'Party', ondelete='CASCADE',
        required=True)
    company = fields.Many2One('company.company', 'Company', ondelete='CASCADE',
        required=True)
    payable_bank_account = fields.Many2One('bank.account',
        'Default Payable Bank Account')
    receivable_bank_account = fields.Many2One('bank.account',
        'Default Receivable Bank Account')
