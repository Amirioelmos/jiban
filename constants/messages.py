

class BotMessage:
    cost_saved = " *{name}* عزیز، هزینه از دسته بندی *{cost_type}* به مبلغ *{amount}* با موفقیت ثبت شد."
    enter_account_of_cost = "لطفا حساب مبدا رو از لیست انتخاب کن:"
    enter_date_of_cost = "لطفا *تاریخ*  این هزینه رو مشخص کن:" \
                         "مثال:۹۷۱۲۱۳"
    enter_amount_of_cost = "میزان *مبلغ پرداختی* رو به ریال وارد کن:"
    choose_cost_category = "از بین موارد زیر، دسته بندی مربوط رو انتخاب کن" \
                           "همچنین میتوانید نام دلخواه خود را وارد نمایید:"
    new_cost = """*{name}* عزیز، لطفا نوع دخل و خرج رو انتخاب کن"""
    thanks_for_payed = "شما به کاربر ویژه بازوی جیبان تبدیل شدید. برید حالشو ببرید."
    invoice_labale = 'نسخه کامل'
    invoice_description = "با خرید نسخه کامل میتوانید از تمامی امکانات بی نظیر بازو استفاده نمایید"
    invoice_text = "خرید نسخه کامل بازوی جیبان"
    please_pay_for_continue = """*{name}* عزیز، برای اینکه بتونی از امکانات کامل این بازو استفاده کنی نیاز به ارتقا به نسخه کامل رو داری. بعد از خرید نسخه کامل همه امکانات بازو برات فعال میشه :)
"""
    new_bank_account_done_by_account_number = """حساب {bank_name} به شماره کارت {cart_number} و شماره حساب{account_number} و با میزان موجودی {remain} ریال به حساب های شما اضافه بشه ؟"""
    enter_account_number = "لطفا شماره حساب مربوط به این حسابت رو وارد کن:"
    new_bank_account_done = """یه خبر خوب! حساب {bank_name} شما به فهرست حساب های شما اضافه شد.
حالا میتونی به صفحه اصلی بازو بری یا یه حساب دیگه اضافه کنی."""
    accept_to_add_bank_account = "حساب {bank_name} به شماره کارت {cart_number} و با میزان موجودی {remain} ریال به حساب های شما اضافه بشه ؟"
    enter_cart_number_of_bank_account = "لطفا شماره کارت مربوط به این حسابت رو وارد کن:"
    enter_remain_of_bank_account = "*مقدار موجودی* حسابت رو به *ریال* و به صورت *عدد* وارد کن:"
    choose_bank_of_account = "لطفا بانک حساب خود را وارد کنید"
    new_cash_account_done = """یه خبر خوب! حساب *{name}* به فهرست حساب های شما اضافه شد.
حالا میتونی به صفحه اصلی بازو بری *یا* یه حساب دیگه اضافه کنی."""

    accept_to_add_your_accounts = "آیا حساب نقدی به نام *{name}* و با میزان موجودی *{amount}* ریال به حساب های شما اضافه بشه ؟"
    enter_amount_of_cash = "مقدار *مبلغی* که الان توی *{name}* داری رو به *ریال* و به صورت *عدد* وارد کن"
    choose_name_for_cash = """لطفا برای پول نقد خودت یک اسم تعیین کن. مثلا *کیف پول* یا *پول روی طاقچه*"""
    choose_service = "*{name}* عزیز،" \
                     " برای شروع لازم هست که یک حساب بانکی یا یک حساب نقد(مثل کیف پول)" \
                     "  تعریف کنی تا بتونم دخل و خرج مربوط به اون حساب رو ثبت کنم."
    enter_name = "لطفا اسم خودت رو وارد کن تا باهم آشنا بشیم :)"
    starter_message = "چه کاری میتونم برات انجام بدم:"
    greeting_message = "من بازوی مدیریت مالی هوشمند جیبان ام. به کمک من میتونی به راحتی و با لذت به مدیریت دخل و خرجات برسی. من با امکاناتی که در اخیارت قرار میدم قطعا شگفت زده ات میکنم، پس هرچه سریعتر شروع کن :)"


class MiniText:

    cash = "حساب نقدی"
    banki = "حساب بانکی"
