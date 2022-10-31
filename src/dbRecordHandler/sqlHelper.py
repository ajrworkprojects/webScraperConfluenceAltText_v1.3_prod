class SQLHelper:
    """Provides a variable of repetitive SQL statements that improves the performance of the db.  These statements should be run before each call to the db.

    ref:  https://phiresky.github.io/blog/2020/sqlite-performance-tuning/
        
    Attributes
    ----------
    SQL_QUERIES : String
        The repetitive SQL statements that improves performance
    
    
    Methods
    ----------
    None
    """

    SQL_QUERIES = """
        PRAGMA journal_mode = WAL;
        PRAGMA synchronous = normal;
        PRAGMA temp_store = memory;
        PRAGMA mmap_size = 30000000000;
        PRAGMA wal_checkpoint(TRUNCATE);
        PRAGMA foreign_keys = ON;
    """