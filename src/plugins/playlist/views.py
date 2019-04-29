# import logging

# from ui.components.table import TableComponent
# from config import config
# import stream

# logger = logging.getLogger('ui')


# class Playlist(TableComponent):

#     def __init__(self):
#         super().__init__()

#         self.columns = config['playlist']['columns']

#         stream.get('library.tracks').subscribe(self.set_tracks)

#     def set_tracks(self, tracks):
#         logger.info('tracks: {}'.format(len(tracks)))
#         self.data = tracks
#         self.refresh()
