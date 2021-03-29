#!/bin/sh -e

# Basically stolen from: https://wildwolf.name/a-simple-script-to-create-systemd-nspawn-alpine-container/

MIRROR="http://dl-cdn.alpinelinux.org/alpine"
VERSION="latest-stable"

[ "$(id -u)" -ne "0" ] && echo "You need to be root"   >&2 && exit 1
# [ -z "$1" ]            && echo "Usage: $0 destination" >&2 && exit 0

dest="/opt/mccli-rootfs"
apkdir="$(mktemp -d)"
[ "$(uname -m)" = "x86_64" ] && guestarch="x86_64" || guestarch="x86"

APKTOOLS="$(wget -q -O - "$MIRROR/$VERSION/main/$guestarch/" | grep -Eo -m 1 '>apk-tools-static[^<]+' | sed 's/[<>]//g')"

wget -q -O - "$MIRROR/$VERSION/main/$guestarch/$APKTOOLS" | tar -xz -C $apkdir || { rm -rf "$apkdir"; exit 1; }
trap 'rm -rf "$apkdir"' EXIT

"$apkdir/sbin/apk.static" -X "$MIRROR/$VERSION/main" -U --arch "$guestarch" --allow-untrusted --root "$dest" --initdb add alpine-base java-common ca-certificates p11-kit-trust p11-kit
"$apkdir/sbin/apk.static" -X "$MIRROR/$VERSION/community" --arch "$guestarch" --allow-untrusted --root "$dest" add openjdk11-jre-headless

echo "$MIRROR/$VERSION/main" > "$dest/etc/apk/repositories"
echo "$MIRROR/$VERSION/community" >> "$dest/etc/apk/repositories"

for i in $(seq 0 10); do
    echo "pts/$i" >> "$dest/etc/securetty"
done

sed -i '/tty[0-9]:/ s/^/#/' "$dest/etc/inittab"
echo 'console::respawn:/sbin/getty 38400 console' >> "$dest/etc/inittab"

for svc in bootmisc hostname syslog; do
    ln -sf "/etc/init.d/$svc" "$dest/etc/runlevels/boot/$svc"
done

for svc in killprocs savecache; do
    ln -sf "/etc/init.d/$svc" "$dest/etc/runlevels/shutdown/$svc"
done

minecraft_gid=$(id -g minecraft)
minecraft_uid=$(id -u minecraft)

sudo systemd-nspawn -UD /opt/mccli-rootfs --private-users=0 sh -c "addgroup -g $minecraft_gid minecraft ; adduser -DG minecraft -u $minecraft_uid minecraft"

echo "Success"