class DuplicateMovieError(Exception):

    def __init__(self, name: str):
        self.name = name
        self.message =  'Movie name "%s" has been already used.' % name
        super().__init__(self.message)


class UnsupportedFileError(Exception):

    def __init__(self, extension: str):
        self.extension = extension
        self.message = '"%s" is an unsupported extension. Supported extensions are ".mp4", ".mp3", ".wav", ".json"' % self.extension
        super().__init__(self.message)
