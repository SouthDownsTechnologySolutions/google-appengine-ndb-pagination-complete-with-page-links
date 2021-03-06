from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor

ITEMS = 10


class TestModelPag(ndb.Model):
    number = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def cursor_pagination(cls, prev_cursor_str, next_cursor_str):
        if not prev_cursor_str and not next_cursor_str:
            objects, next_cursor, more = cls.query().order(cls.number).fetch_page(ITEMS)
            prev_cursor_str = ''
            if next_cursor:
                next_cursor_str = next_cursor.urlsafe()
            else:
                next_cursor_str = ''
            next_ = True if more else False
            prev = False
        elif next_cursor_str:
            cursor = Cursor(urlsafe=next_cursor_str)
            objects, next_cursor, more = cls.query().order(cls.number).fetch_page(ITEMS, start_cursor=cursor)
            prev_cursor_str = next_cursor_str
            next_cursor_str = next_cursor.urlsafe()
            prev = True
            next_ = True if more else False
        elif prev_cursor_str:
            cursor = Cursor(urlsafe=prev_cursor_str)
            objects, next_cursor, more = cls.query().order(-cls.number).fetch_page(ITEMS, start_cursor=cursor)
            objects.reverse()
            next_cursor_str = prev_cursor_str
            prev_cursor_str = next_cursor.urlsafe()
            prev = True if more else False
            next_ = True

        return {'objects': objects, 'next_cursor': next_cursor_str, 'prev_cursor': prev_cursor_str, 'prev': prev,
                'next': next_}

    @classmethod
    def offset_pagination(cls, offset):
        """Pagination through query offset"""

        if offset:
            try:
                offset = int(offset)
            except ValueError:
                offset = 0
        objects, next_cursor, more = cls.query().order(cls.number).fetch_page(ITEMS, offset=offset)
        total_records = TestModelPag.query().count()

        prev_offset = max(offset - ITEMS, 0)
        prev = True if offset else False
        next_ = True if more else False
        next_offset = ''
        if next_:
            next_offset = offset + ITEMS

        links = []
        for number in range(total_records):
            if number % ITEMS == 0:
                check = False
                print "number: ", number, "    offset: ", offset
                if number == offset:
                    check = True
                if number > offset + 30 or offset - number > 30:
                    print number
                else:
                    page_number = number / ITEMS
                    links.append([number, check, page_number])
        print links
        last_link=total_records-ITEMS
        return {'objects': objects,
                'prev': prev,
                'next': next_,
                'prev_offset': prev_offset,
                'next_offset': next_offset,
                'Total_Records': total_records,
                'number_of_link': ITEMS,
                'links': links,
                'last':last_link
                }
