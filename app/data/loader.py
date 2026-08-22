import os
import pandas as pd
from typing import Dict, Any, List, Optional
from app.config import settings
from app.security.access_control import authorize


class DataRepository:
    def __init__(self, excel_path: Optional[str] = None):
        # Use settings if no path is provided. Fallback to EXCEL_FILE_PATH if EXCEL_PATH is not in settings.
        self.excel_path = excel_path or getattr(settings, 'EXCEL_FILE_PATH', getattr(settings, 'EXCEL_PATH', './data/ParcelPilot_Assessment_Data.xlsx'))
        
        # Ensure path is absolute to avoid relative directory issues
        if not os.path.isabs(self.excel_path):
            self.excel_path = os.path.abspath(self.excel_path)
            
        self._load_data()

    def _load_data(self):
        if not os.path.exists(self.excel_path):
            raise FileNotFoundError(f"Excel dataset not found at: {self.excel_path}")
            
        # FIX: Explicitly specify engine="openpyxl"
        xls = pd.ExcelFile(self.excel_path, engine="openpyxl")
        self.readme_df = pd.read_excel(xls, sheet_name="README")
        self.accounts_df = pd.read_excel(xls, sheet_name="accounts")
        self.orders_df = pd.read_excel(xls, sheet_name="orders")
        self.tickets_df = pd.read_excel(xls, sheet_name="tickets")

        # Read snapshot timestamp
        self.snapshot_time = str(self.readme_df.iloc[0, 1])

    def get_account(self, account_id: str, user_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        authorize(user_context, resource_account_id=account_id, action="read_account")
        row = self.accounts_df[self.accounts_df["account_id"] == account_id]
        if row.empty:
            return None
        return row.iloc[0].to_dict()

    def get_order(self, order_id: str, user_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        row = self.orders_df[self.orders_df["order_id"] == order_id]
        if row.empty:
            return None
        order_dict = row.iloc[0].to_dict()
        authorize(user_context, resource_account_id=order_dict["account_id"], action="read_order")
        return order_dict

    def get_ticket(self, ticket_id: str, user_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        row = self.tickets_df[self.tickets_df["ticket_id"] == ticket_id]
        if row.empty:
            return None
        ticket_dict = row.iloc[0].to_dict()
        authorize(user_context, resource_account_id=ticket_dict["account_id"], action="read_ticket")
        return ticket_dict

    def list_orders(self, account_id: Optional[str], user_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        target_account = account_id or user_context.get("account_id")
        authorize(user_context, resource_account_id=target_account, action="list_orders")

        if target_account:
            filtered = self.orders_df[self.orders_df["account_id"] == target_account]
        else:
            filtered = self.orders_df
        return filtered.to_dict(orient="records")

    def list_tickets(self, account_id: Optional[str], user_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        target_account = account_id or user_context.get("account_id")
        authorize(user_context, resource_account_id=target_account, action="list_tickets")

        if target_account:
            filtered = self.tickets_df[self.tickets_df["account_id"] == target_account]
        else:
            filtered = self.tickets_df
        return filtered.to_dict(orient="records")


# FIX: Do not hardcode the path. Let it use the default settings automatically.
repo = DataRepository()