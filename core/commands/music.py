import io
from discord.ext import commands
from discord import File
import wavelink
from datetime import timedelta


class Music(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.wavelink_connect())
        print("looped node")

    async def wavelink_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.bot, host="lava.link", port=80, password="dismusic"
        )

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.identifier} is ready! Connected {node.is_connected()}")

    @commands.Cog.listener()
    async def on_wavelink_track_end(
        self, player: wavelink.Player, track: wavelink.YouTubeTrack, reason: str
    ):
        ctx = player.ctx
        # vc: player = ctx.voice_client
        vc: player = ctx.voice_client

        if vc.loop:
            return await vc.play(track)

        print(vc.queue)
        try:
            nt = vc.queue.get()
            await vc.play(nt)
            await ctx.send(
                f"""
Сейчас играет: **{nt.title}**

||Информация о песне которая проигрывается:||

||Позиция песни: {nt.info.get("position")}||
||Название песни: {nt.title}||
||Время: {timedelta(seconds=nt.length)}||
||URL: {nt.uri}||
    """
            )
        except wavelink.QueueEmpty:
            return

    @commands.group(name="music")
    async def music(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                """
Информация
```
play [название или ссылка на песню]
stop
volume [проценты (от 0 до 100)]
pause
resume
loop
np
exit
```
            """
            )

    @music.command(name="play")
    async def _play(self, ctx: commands.Context, query: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            player: wavelink.Player = await ctx.author.voice.channel.connect(
                cls=wavelink.Player
            )
        else:
            player: wavelink.Player = ctx.voice_client

        send = await ctx.reply("Ожидайте...")

        player.ctx = ctx
        setattr(player, "loop", False)
        print(player.queue.is_empty)
        if player.queue.is_empty and not player.is_playing():
            await player.play(query)
            await send.edit(content=f"Сейчас проигрывается: **{query.title}**")
        else:
            # await player.queue.put_wait(query)
            await player.queue.put_wait(query)
            await send.edit(f"Добавлена песня **{query.title}** в список")
    @music.command(name="volume")
    async def _volume(self, ctx, volume: int):
        if not ctx.voice_client:
            return await ctx.reply(
                f"А зачем мне изменять звук, если я не подключился к каналу? Запустите для начала песню, и попробуйте снова"
            )

        else:
            player: wavelink.Player = ctx.voice_client

        send = await ctx.reply("Ожидайте...")
        if volume > 100:
            await send.edit(content="Нельзя ставить звук больше 100%")
        elif volume < 0:
            await send.edit(content="Нельзя ставить звук меньше 0%")
        else:
            await player.set_volume(volume)
            await send.edit(content=f"Успешно изменил громкость на {volume}%")

    @music.command(name="np")
    async def _np(self, ctx):
        if not ctx.voice_client:
            return await ctx.send(
                f"Я не подключен к каналу. Включите песню и попробуйте снова"
            )

        else:
            player: wavelink.Player = ctx.voice_client

        if not player.is_playing():
            return await ctx.reply("Сейчас никакая музыка не воспроигрывается")

        await ctx.reply(
            f"""
Информация о песне:
```css
Позиция песни: {player.track.info.get("position")}
Название песни: {player.track.title}
Время: {timedelta(seconds=player.track.length)}
URL: {player.track.uri}
```
        """
        )

    @music.command(name="stop")
    async def _stop(self, ctx):
        if not ctx.voice_client:
            return await ctx.send(
                f"Я не подключен к каналу. Включите песню и попробуйте снова"
            )

        else:
            player: wavelink.Player = ctx.voice_client

        if not player.is_playing():
            return await ctx.reply("Сейчас никакая музыка не воспроигрывается. Отмена")

        await player.stop()
        await ctx.reply("Музыка остановлена")

    @music.command(name="pause")
    async def _pause(self, ctx):
        if not ctx.voice_client:
            return await ctx.send(
                f"Я не подключен к каналу. Включите песню и попробуйте снова"
            )

        else:
            player: wavelink.Player = ctx.voice_client

        if not player.is_playing():
            return await ctx.reply("Сейчас никакая музыка не воспроигрывается. Отмена")

        await player.pause()
        await ctx.reply("Музыка приостановлена")

    @music.command(name="resume")
    async def _resume(self, ctx):
        if not ctx.voice_client:
            return await ctx.send(
                f"Я не подключен к каналу. Включите песню и попробуйте снова"
            )

        else:
            player: wavelink.Player = ctx.voice_client

        if not player.is_playing():
            return await ctx.reply("Сейчас никакая музыка не воспроигрывается. Отмена")

        await player.resume()
        await ctx.reply("Музыка возобновлена")

    @music.command(name="exit")
    async def _exit(self, ctx):
        if not ctx.voice_client:
            return await ctx.send(
                f"Я не подключен к каналу. Включите песню и попробуйте снова"
            )

        else:
            player: wavelink.Player = ctx.voice_client

        await player.disconnect()
        await ctx.reply("Я отключился от голосового чата")

    @music.command(name="loop")
    async def _loop(self, ctx):
        if not ctx.voice_client:
            return await ctx.send(
                f"Я не подключен к каналу. Включите песню и попробуйте снова"
            )

        else:
            player: wavelink.Player = ctx.voice_client
        if not player.is_playing():
            return await ctx.reply("Сейчас никакая музыка не воспроигрывается. Отмена")

        try:
            player.loop = True
        except:
            setattr(player, "loop", False)

    @music.command(name="queue")
    async def _queue(self, ctx):
        if not ctx.voice_client:
            return await ctx.send(
                f"Я не подключен к каналу. Включите песню и попробуйте снова"
            )

        else:
            player: wavelink.Player = ctx.voice_client
        if player.queue.is_empty:
            return await ctx.reply("Список пуст")

        queue = player.queue.copy()
        await ctx.reply(
            content="Список песен ||в файле||",
            file=File(fp=io.StringIO("\n".join([f for f in queue]))),
        )


def setup(bot) -> None:
    bot.add_cog(Music(bot))
