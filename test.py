class Chapter(object):
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

class Book(object):
    chapterCount = 0
    def __init__(self, title, chapters):
        self.title = title
        self.chapters = chapters
        self.chapterCount = len(chapters)

    def getPageCount(self):
        count = 0
        for chapter in self.chapters:
            count += chapter.pages
        return count
    
    def getChapter(self, n):
        return self.chapters[n]

def testBookAndChapterClasses():
    print("\tTesting Book and Chapter classes...", end="")
    chapterA = Chapter('I love CS!', 30) # chapter title, # of pages
    chapterB = Chapter('So do I!', 15)
    book1 = Book('CS is Fun!', [chapterA, chapterB]) # book title, chapters
    book2 = Book('The Short Book', [ Chapter('Quick Read!', 5) ])

    assert(book1.chapterCount == 2)
    assert(book1.getPageCount() == 45)
    assert(book2.chapterCount == 1)
    assert(book2.getPageCount() == 5)
    assert(book1.getChapter(0).title == 'I love CS!')
    assert(book1.getChapter(1).title == 'So do I!')
    assert(book2.getChapter(0).title == 'Quick Read!')

    # Move chapter 0 from book1 to the end of book2
    # so moveChapter always moves to the end of the target book.
    book1.moveChapter(0, book2)

    assert(book1.chapterCount == 1)
    assert(book1.getPageCount() == 15)
    assert(book1.getChapter(0).title == 'So do I!')
    assert(book2.chapterCount == 2)
    assert(book2.getPageCount() == 35)
    assert(book2.getChapter(0).title == 'Quick Read!')
    assert(book2.getChapter(1).title == 'I love CS!')
    print("Passed!")


testBookAndChapterClasses()