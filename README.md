# interface_exporter
Prometheus exporter for collecting interface statuses.

Status check is based on values from /sys/class/net. Possible values:

-    1 - if [operstate](https://github.com/torvalds/linux/blob/master/Documentation/ABI/testing/sysfs-class-net#L210) is *up*.
-    1 - if [operstate](https://github.com/torvalds/linux/blob/master/Documentation/ABI/testing/sysfs-class-net#L210) is *unknown* and [carrier](https://github.com/torvalds/linux/blob/master/Documentation/ABI/testing/sysfs-class-net#L70) is *1*. It's made for virtual drivers like TUN/TAP or if    driver doesn't support/show operstate
-    0 - in other cases

## Building and running
Use docker-complose 
```
docker-compose up -d
```

