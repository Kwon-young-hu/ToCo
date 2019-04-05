/*
 */

#ifndef UCI_CONF_H
#define UCI_CONF_H

#include	<uci.h>

/*
 * @opt
 * get: <config>.<section>[.<option>]
 * set: <config>.<section>[.<option>]
 * commit: [<config>](NULL: all configs.)
 * changes: [<config>](NULL: all configs.)
 * revert: <config>[.<section>[.<option>]]
 * getlist: <config>.<section>[.<option>]
 * addlist: <config>.<section>.<option>
 * delist: <config>.<section>.<option> 
 * add: <config>
 * del: <config>.<section>[.<option>] 
 */
extern int	config_get(char *opt, char *val, int size);
extern int	config_set(char *opt, char *val);
extern int	config_changes(char *opt);
extern int	config_revert(char *opt);
extern int	config_commit(char *opt);

/*
 * XXX: keep in mind
 * @val is fixed sized 2-dimen. array AND 
 * @LIST_BUFSIZ must be used
 * usage: config_getlist(opt, val, LIST_BUFSIZ(val)); 
*/
#define LIST_BUFSIZ(_a) (int)sizeof((_a)[0]), (int)(sizeof((_a)) / sizeof((_a)[0]))
extern int	config_getlist(char *opt, char *val, ...);

extern int	config_addlist(char *opt, char *val);
extern int	config_dellist(char *opt, char *val);
extern int	config_add(char *conf, char *sec, char *val, int size);
extern int	config_del(char *opt, char *val);

#endif /* UCI_CONF_H */
